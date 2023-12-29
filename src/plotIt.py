import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



countriesPirates = []

df = pd.read_csv("resIpAddresses.csv", index_col=False)



countries = ['United States', 'Russia', 'Germany', \
    'India', 'Turkey', 'Philippines', 'Spain', \
        'Bulgaria', 'Australia', 'Brazil', \
            'South Africa', 'Burundi', 'China', \
                'France', 'Algeria']

# https://www.cia.gov/the-world-factbook/field/population/country-comparison/
countriesPopulation = [ 339665118, 141698923, 84220184, \
    1399179585, 83593483, 116434200, 47222613,\
        6827736, 26461166, 218689757, 58048332,\
            13162952, 1413142846, 68521974, 44758398
]


for i, country in enumerate(countries):
    value = (len(df[df["country"] == country])/countriesPopulation[i])*100
    value = f'{value:.20f}'
    value = value if value != 0 else 0
    countriesPirates.append(value)


countriesGDP = [76329.6, 15270.7, 48718.0, 2410.9, \
    10674.5, 3498.5, 29674.5, 13974.4, 65099.8, \
    8917.7, 6766.5, 259.0, 12720.2, 40886.3, 4342.6\
]


# These lines order countries based on GDP and Piracy respectively
countriesGDPDict = list(dict(sorted(dict(zip(countriesGDP, countries)).items())).values())
countriesPiratesDict = list(dict(sorted(dict(zip(countriesPirates, countries)).items())).values())

# These lines give a numeric rank to each country for GDP and Piracy
countriesGDPRanking = {country: rank for rank, country in enumerate(countriesGDPDict)}
countriesPiratesRanking = {country: rank for rank, country in enumerate(countriesPiratesDict)}

# We subtract one rank from the other here and square the result
rankingDiffs = {country: (rankGDP - countriesPiratesRanking[country])**2 for country, rankGDP in countriesGDPRanking.items()}

# This sums the resulting numbers
rankingSum = sum(rankingDiffs.values())

# Finally, we can calculate the correlation coefficient using the forumla given to us
numberCountries = len(countries)
correlationCoefficient = 1 - (6*rankingSum)/(numberCountries**3 - numberCountries)
correlationCoefficient = round(correlationCoefficient, 2) # Here, we round the result
print(correlationCoefficient)  # The result shown to us is 0.3

countriesWithPirates = [country+f"-{str(countriesPirates[i])}" for i, country in enumerate(countries)]
countriesGDPMap = dict(zip(countriesGDP, countriesWithPirates))
countriesGDPMap = dict(sorted(countriesGDPMap.items()))

for gdp, country in countriesGDPMap.items():
    # print(str(gdp)+f" - {country.split('-')[0]} - {country.split('-')[1][:10]}%")
    pass

countriesWithGdp = [country+f"\n({str(countriesGDP[i])}$)" for i, country in enumerate(countries)]



countryCount = str(df["country"].value_counts().head(50))
# Fixing random state for reproducibility
np.random.seed(92143)


N = 5
x = [country.split("-")[0]+f"\n({list(countriesGDPMap.keys())[i]}$)" for i, country in enumerate(countriesGDPMap.values())]
y = [float(country.split("-")[1]) for country in countriesGDPMap.values()]
colors = np.random.rand(len(countries))
area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

plt.scatter(x, y, s=200, c=colors, alpha=0.5)
plt.title("Piracy rates compared to GDP per Capita")
plt.xlabel("Countries with GDP per Capita")
plt.ylabel("Percentage of population pirating from fitgirl")
plt.show()