import textwrap
import pandas as pd
from src.logger import Logger


class PriceCleanupHelper:

    def __indent(self, text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)

    def clean_prices(self, dataframe, column_name, filename):
        currency_conversion_error_df = dataframe.rename(columns={column_name: 'Violating Character'})
        price_conversion_df = dataframe

        # Find alphanumerical characters filtered out by regex (except euro character) and place into error dataframe
        currency_conversion_error_df['Violating Character'] = currency_conversion_error_df[
            'Violating Character'].str.findall(r"[a-zA-Z]")

        # Filter out empty string arrays returned by regex findall
        currency_conversion_error_df = currency_conversion_error_df[
            currency_conversion_error_df['Violating Character'].str.len() > 0]
        # print(len(currency_conversion_error_df))
        if len(currency_conversion_error_df) > 0:
            error_string = "Price conversion error found in: " + filename + "\n" \
                           + self.__indent(currency_conversion_error_df.to_string()
                                           + "\nViolating character is removed and resulting price will be migrated to target.",
                                           30)

            print(error_string)
            Logger().error(error_string)

        # Remove alphanumeric characters from prices.
        price_conversion_df['Extra Price'] = price_conversion_df['Extra Price'].str.replace(r"[a-zA-Z€ ]", '', regex=True)
        price_conversion_df["Extra Price"] = pd.to_numeric(price_conversion_df["Extra Price"])
        # uniform capitalization of ingredient names.
        price_conversion_df['Ingredient'] = price_conversion_df['Ingredient'].str.title()