import os
from app.api import rms
from flask import request, abort
from .files import file_operation, error_messages
from app.api.utils import token_required, custom_make_response,\
     allowed_extension


# getting environment variables
KEY = os.environ.get("SECRET_KEY")
PAYMENTS_UPLOAD_FOLDER = os.environ.get("PAYMENTS_FOLDER")


@rms.route("/auth/upload/payments", methods=["POST"])
@token_required
def upload_payment(user):
    """
    upload  a payment for a given project
    only the creator can upload a payment
    """
    if user["role"] != "Creator":
        abort(
            custom_make_response(
                "error",
                "You are not authorized to carry out this action.", 403
            )
        )
    try:
        receivedFile = request.files["paymentExcelFile"]
        if allowed_extension(receivedFile.filename) and receivedFile:
            return file_operation(
                receivedFile,
                PAYMENTS_UPLOAD_FOLDER,
                "Payment",
                user["companyId"],
                user["id"],
            )
        return custom_make_response(
            "error",
            "Only excel files are allowed, please select\
                 a payment excel file & try again.",
            400,
        )
    except Exception as e:
        error_messages(e, "payment")
