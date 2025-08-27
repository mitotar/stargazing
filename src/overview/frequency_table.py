

def create_frequency_table(df):
    df_count = df.resample("YE").count()

    years = [x.strftime("%Y") for x in df_count.index]
    counts = [df_count.loc[x].number_of_objects.values[0] for x in years]

    years.append("Total")
    counts.append(sum(counts))

    return dict(zip(years, counts))


if __name__ == "__main__":
    pass
