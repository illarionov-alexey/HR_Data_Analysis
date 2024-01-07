# your code here. the dataset is already loaded as sales_data.

print(sales_data.query(' (Category == "Furniture" | Category == "Technology") & Sales < 25 '))