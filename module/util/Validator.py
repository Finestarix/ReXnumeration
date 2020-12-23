def isIPv4(target):
    try:
        return str(int(target)) == target and 0 <= int(target) <= 255
    except Exception:
        return False


def isValidRange(value, minVal, maxVal):
    try:
        return minVal <= int(value) <= maxVal
    except Exception:
        return False
