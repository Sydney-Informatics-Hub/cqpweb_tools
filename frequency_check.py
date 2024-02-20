# compare frequency lists


PROD_FREQ = "testing/frequency_prod.txt"
DEV_FREQ = "testing/frequency_dev.txt"


def load_freq_list(filename):
    freqs = {}
    with open(filename, "r") as fh:
        for line in fh.readlines():
            bits = line[:-1].split("\t")
            if len(bits) == 3:
                try:
                    freq = int(bits[2])
                    token = bits[1].lower()
                    freqs[token] = freq
                except ValueError:
                    # if the third column isn't an int, skip
                    pass
    return freqs


def main():
    f_prod = load_freq_list(PROD_FREQ)
    f_dev = load_freq_list(DEV_FREQ)

    print(f"Checking all tokens from {PROD_FREQ} ...")
    for token, count in f_prod.items():
        if token not in f_dev:
            print(f"{token} not found in {DEV_FREQ}")
        else:
            if f_dev[token] != f_prod[token]:
                msg = f"Frequency for token '{token}' is {f_dev[token]}"
                msg += f"(expected {f_prod[token]})"
                print(msg)
            f_dev.pop(token)

    print("Done.")

    if len(f_dev) > 0:
        print(f"Tokens in {DEV_FREQ} not found in prod:")
        print(f_dev)
    else:
        print("No leftover words in dev.")


if __name__ == "__main__":
    main()
