def valToDuty(val):
	ratio = val / 4095
	duty = int(ratio * 65535)
	return duty