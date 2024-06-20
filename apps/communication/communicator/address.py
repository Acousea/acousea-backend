class Address:
    BACKEND = 0x00
    LOCALIZER = 0x01      # 0b01000000
    DRIFTER = 0x02        # 0b10000000
    PI3 = 0x03            # 0b11000000
    SENDER_MASK = 0xC0    # 0b11000000
    RECEIVER_MASK = 0x30  # 0b00110000
