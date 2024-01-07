import pandas as pd

penguins_dict = {'species': {0: 'Adelie', 1: 'Gentoo', 2: 'Chinstrap', 
                             3: 'Gentoo', 4: 'Chinstrap', 5: 'Adelie', 
                             6: 'Adelie', 7: 'Adelie'},
                 'island': {0: 'Torgersen', 1: 'Biscoe', 2: 'Dream', 
                            3: 'Biscoe', 4: 'Dream', 5: 'Dream', 
                            6: 'Torgersen', 7: 'Biscoe'}, 
                 'body_mass_g': {0: 4250.0, 1: 5200.0, 2: 4400.0, 3: 4550.0,
                                 4: 3700.0, 5: 3550.0, 6: 3250.0, 7: 4275.0}}

weighted_penguins = pd.DataFrame(penguins_dict)


# your code here

weighted_penguins = weighted_penguins[weighted_penguins.body_mass_g  >= 3300], 'thin penguin' )
weighted_penguins = weighted_penguins.where(weighted_penguins.body_mass_g  <= '4000', 'plump penguin')
print(weighted_penguins)