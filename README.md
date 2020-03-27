# fossifreefund_compiler
sorts through fossilfreefunds.org api to retrieve info on top funds based on user criteria

Then a series of lines filters through that data based on the following metrics (just what I thought up quickly, feel free to change once you pull down):
-the fund must have an A grade in deforestation and fossil fuels
-the fund must have a badge count of 5
-the fund must have a 90% or above 'percent rated' score (this means that over 90% of the funds assets were able to be evaluated by fossilfreefunds.org)
-the funds must be 'socially responsible' (SRI)
-the fund must have a sustainability metric
-the fund must be in the top 30% based on investment in fossilfreefund's Clean 200 companies (see here for more details)
-the fund must be in the top 10% of various fossil fuel and utility metrics
-the fund must be in the top 30% based on carbon intensity profile

The last three happen after the the first five filters have been applied.

Once we have the filtered funds, we still have lots of what are essentially duplicates (minor variations on the same family of funds). The script groups each fund by its 'family' and then selects the best performing fund by its 5 year trailing returns.

Real estate and health care funds are ignored as they tend to crowd the field and I wasn't interested in investing in them.

The script outputs three csv's:
- a giant dataframe of all info on all availble stocks
- a filtered dataframe with all info for qualifying stocks
- a filtered dataframe with select info and cleaned up names, etc.



Enjoy and please offer feedback!