import requests

__author__ = 'whelks_chance'

# Brain child of /u/Athox on Reddit, via /r/ProgrammerHumor
# https://www.reddit.com/r/ProgrammerHumor/comments/2t1vlf/why_you_dont_let_programmers_design_train_stations/cnv1bgw


def encode(block_of_text, secret, pad=8):
    if len(block_of_text.replace(' ', '')) < (len(secret.replace(' ', '')) * pad):
        raise Exception('Need more open text')

    all_bin_vals = ''
    for letter in secret:
        # print letter
        ord_value = ord(letter)
        # print ord_value
        bin_ord = bin(ord_value)
        bin_ord = bin_ord[2:]

        bin_ord = bin_ord.zfill(pad)
        # print bin_ord

        for bin_val in bin_ord:
            # print bin_val
            all_bin_vals += bin_val
    # print all_bin_vals

    encoded_text = ''
    pointer = 0
    for to_encode in block_of_text.lower():
        if to_encode.isalnum():
            if pointer >= len(all_bin_vals):
                encoded_text += to_encode.lower()
                pointer = 0
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


def decode(encrypted, pad=8):
    encrypted = encrypted.replace(' ', '')
    stripped = ''
    for ch in encrypted:
        if ch.isalnum():
            stripped += ch
    encrypted = stripped

    decoded = ''
    for eight_char_block in split_by_n(encrypted, pad):
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


# a test case with a high end unicode character which requires padding to 11 bits per char instead of regular 8
def test():

    text_block = u'this is a long piece of text to hide some ' \
                 u'words in, because I  \u0A86 apparently don\'t have anything better to do and now this ' \
                 u'sentence needs to be longer. There is a limitation $that there needs to be $padding (default 8)' \
                 u' times more useless text than secret message.' \
                 u' Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' \
                 u'Sed nisi urna, auctor vitae imperdiet vel, pellentesque et nisl. '
    the_secret = u'password is : hunter2'

    encoded = encode(text_block, the_secret, pad=11)
    print encoded
    print decode(encoded, pad=11)


def grab_ipsum(num_paras):
    return requests.get('http://loripsum.net/api/plaintext/prude/long/' + str(num_paras)).text


def hide_text_ipsum(secret, pad=8):
    # assume <400 char per paragraph ipsum minimum
    a = len(secret) * pad
    b = (a/400) + 1
    return encode(grab_ipsum(b), secret, pad)

## yup, I encoded a chunk of ipsum in a larger chunk of ipsum...
# enc = hide_text_ipsum(grab_ipsum(1))

enc = hide_text_ipsum('This is a secret which should be hidden in a big block of ipsum password : hunter2')
print enc
print decode(enc)