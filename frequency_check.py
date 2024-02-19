# compare frequency lists


PROD_FREQ = "frequency_prod.txt"
DEV_FREQ = "frequency_list_dev6.txt"

def load_freq_list(filename):
    freqs = {}
    with open(filename, "r") as fh:
        for line in fh.readlines():
            bits = line[:-1].split("\t")
            if len(bits) == 3:
                token = bits[1].lower()
                freqs[token] = int(bits[2])
    return freqs


f_prod = load_freq_list(PROD_FREQ)
f_dev = load_freq_list(DEV_FREQ)

for token, count in f_prod.items():
    if token not in f_dev:
        print(f"Not found in dev: {token}")
    else:
        if f_dev[token] != f_prod[token]:
            print(f"Count out for token {token} {f_dev[token]}")
        f_dev.pop(token)

if len(f_dev) > 0:
    print("Tokens in dev not found in prod:")
    print(f_dev)
