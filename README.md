# SquidAnalyzer Mail Report

This script must be run after squid-analyzer. Its main function is to report the Top 10 Users by email.

## How To?

You only need to replace the corresponding $VARIABLES with the appropriate values.

* $SRC_EMAIL = The source email. The account from which the email will be sent.
* $PASSWD_SRC_EMAIL = The password to the source email.
* $DEST_EMAIL = The destination email. The account that will receive the email.
* $SERVER_ADDRESS = The address from the mail server. (e.g. mail.local.com)
* $PORT = The port correspondent to the mail server. (e.g. 25)
