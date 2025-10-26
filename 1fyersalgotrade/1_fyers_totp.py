from pyotp import TOTP

otpSecret = "ABCDEF"
token = TOTP(otpSecret).now()
print("OTP:", token)