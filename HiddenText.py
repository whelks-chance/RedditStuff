__author__ = 'whelks_chance'

# Brain child of /u/Athox on Reddit, via /r/ProgrammerHumor
# https://www.reddit.com/r/ProgrammerHumor/comments/2t1vlf/why_you_dont_let_programmers_design_train_stations/cnv1bgw


def encode(block_of_text, secret):
    if len(block_of_text.replace(' ', '')) < (len(secret.replace(' ', '')) * 8):
        raise Exception('Need more open text')

    all_bin_vals = ''
    for letter in secret:
        # print letter
        ord_value = ord(letter)
        # print ord_value
        bin_ord = bin(ord_value)
        bin_ord = bin_ord[2:]

        bin_ord = bin_ord.zfill(8)
        # print bin_ord

        for bin_val in bin_ord:
            # print bin_val
            all_bin_vals += bin_val
    print all_bin_vals

    encoded_text = ''
    pointer = 0
    for to_encode in block_of_text.lower():
        if to_encode.isalnum():
            if pointer >= len(all_bin_vals):
                encoded_text += to_encode.lower()
            else:
                if all_bin_vals[pointer] == '1':
                    encoded_text += to_encode.upper()
                else:
                    encoded_text += to_encode.lower()
            pointer += 1
        else:
            encoded_text += to_encode
    return encoded_text


def split_by_n(seq, n):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]


def decode(encrypted):
    encrypted = encrypted.replace(' ', '')
    stripped = ''
    for ch in encrypted:
        if ch.isalnum():
            stripped += ch
    encrypted = stripped

    decoded = ''
    for eight_char_block in split_by_n(encrypted, 8):
        # print eight_char_block
        block_bin = ''
        for letter in eight_char_block:
            if letter.lower() == letter:
                block_bin += '0'
            else:
                block_bin += '1'
        # print block_bin
        # print int(block_bin, 2)
        decoded_char = chr(int(block_bin, 2))
        if ord(decoded_char) != 0:
            decoded += decoded_char
    return decoded

text_block = u'this is a long piece of text to hide some ' \
             u'words in, because I apparently don\'t have anything better to do and now this ' \
             u'sentence needs to be longer. There is a limitation $that there needs to be 8 times more useless ' \
             u'text than secret message.'
the_secret = u'password is : hunter2'

encoded = encode(text_block, the_secret)
print encoded
print decode(encoded)
