import os
import asyncio
from typing import Optional

from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123.client import Client as Client
from alibabacloud_dm20151123 import models as models
from alibabacloud_tea_util import models as util_models

from fastapi import HTTPException

from oss.src.utils.env import env


config = open_api_models.Config(
    type='access_key',
    access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
    access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
)
config.endpoint = 'dm.aliyuncs.com'
client = Client(config)

def read_email_template(template_file_path):
    """
    Function to read the HTML template from the file
    """

    # Get the absolute path to the template file
    script_directory = os.path.dirname(os.path.abspath(__file__))
    absolute_template_file_path = os.path.join(script_directory, template_file_path)

    with open(absolute_template_file_path, "r") as template_file:
        return template_file.read()


async def send_email(
    to_email: str, subject: str, html_content: str, from_email: str
) -> bool:
    """
    Send an email to a user using Alibaba Cloud DirectMail service.

    Args:
        to_email (str): The email address to send the email to.
        subject (str): The subject of the email.
        html_content (str): The HTML content of the email.
        from_email (str): The email address to send the email from.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Raises:
        HTTPException: If there is an error sending the email.
    """
    
    single_send_mail_request = models.SingleSendMailRequest(
        account_name=from_email,
        address_type=1,
        reply_to_address=False,
        to_address=to_email,
        subject=subject,
        html_body=html_content
    )
    runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        client.single_send_mail_with_options(single_send_mail_request, runtime)
        return True
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
