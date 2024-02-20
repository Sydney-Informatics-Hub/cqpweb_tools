# compare frequency lists


PROD_FREQ = "testing/frequency_prod_20240220.txt"
DEV_FREQ = "testing/frequency_dev_20240220.txt"


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

print("Checking all tokens from prod...")
for token, count in f_prod.items():
    if token not in f_dev:
        print(f"Not found in dev: {token}")
    else:
        if f_dev[token] != f_prod[token]:
            print(f"Count out for token {token} {f_dev[token]}")
        f_dev.pop(token)

print("Done.")

if len(f_dev) > 0:
    print("Tokens in dev not found in prod:")
    print(f_dev)
else:
    print("No leftover words in dev.")
