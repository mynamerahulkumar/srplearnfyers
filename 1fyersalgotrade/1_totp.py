from pyotp import TOTP

otpSecret = "Z55HB87108"
token = TOTP(otpSecret).now()
print("OTP:", token)