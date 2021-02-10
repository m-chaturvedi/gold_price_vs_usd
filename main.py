from datetime import datetime
import pandas
import matplotlib.pyplot as plt

troy_ounce_in_gm = 31.1034768


def main():
    gold_price_file_path = "gold_prices.csv"
    usd_price_file_path = "usd_inr.csv"

    gold_table = pandas.read_csv(gold_price_file_path, sep='\t')
    dollar_table = pandas.read_csv(usd_price_file_path, sep=',')
    all_data = []

    for date_str, gold_usd in zip(gold_table.Date, gold_table.USD):
        dt = datetime.strptime(date_str, '%m/%d/%Y')
        date_new_format = dt.strftime("%Y-%m-%d")
        if int(dt.strftime("%Y")) < 2000:
            continue
        if int(dt.strftime("%Y")) > 2020:
            continue
        row = dollar_table[dollar_table["Date"] == date_new_format]
        if len(row) > 0:
            assert len(row.Close.values) == 1
            dollar_rate = row.Close.values[0]
            row_dict = {"Date": dt.strftime("%m-%Y"),
                        "Gold_USD": gold_usd, "Ex": dollar_rate,
                        "Gold_INR": gold_usd * dollar_rate}
            all_data.append(row_dict)

    all_data = pandas.DataFrame(all_data)

    plt.plot(all_data.Date.values,
             all_data.Gold_INR.values / all_data.Gold_INR.values[0],
             label="Gold_INR")
    plt.plot(all_data.Date.values,
             all_data.Ex.values / all_data.Ex.values[0], label="Exchange")
    plt.plot(all_data.Date.values,
             all_data.Gold_USD.values / all_data.Gold_USD.values[0],
             label="Gold_USD")

    plt.xticks([all_data.Date[x]
                for x in range(all_data.shape[0]) if x % 15 == 0])
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
