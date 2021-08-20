from pandas.api.types import CategoricalDtype

category_chr = (
    '1', '01', '2', '02', '3', '03', '4', '04', '5', '05',
    '6', '06', '7', '07', '8', '08', '9', '09',
    '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    '21', '22', '23', 'X', 'x', 'Y', 'y', 'M', 'm')


category_chr_order = CategoricalDtype(
    category_chr,
    ordered=True
)

