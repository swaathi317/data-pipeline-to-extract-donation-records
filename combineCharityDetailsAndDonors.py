# import libraries
import pandas as pd
import os


def main():

    # read donor details folder
    donor_details_folder_path = './data_extraction/donor_details/'
    donor_files = [file for file in os.listdir(
        donor_details_folder_path) if file.endswith('.csv')]

    # read each csv file and add to df
    charities_arr = []
    for file in donor_files:
        df = pd.read_csv(donor_details_folder_path + file)
        charities_arr.append(df)

    # concatenate dfs
    combined_charities_df = pd.concat(charities_arr, ignore_index=True)

    # write to CSV file
    combined_charities_df.to_csv(
        './data_extraction/combinedDonorDetailsData.csv', index=False)


if __name__ == '__main__':
    main()
