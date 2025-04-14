import pandera as pa
from pandera import Column, DataFrameSchema, Check

# define dataset schema based on observed values
schema = DataFrameSchema({
    "age": Column(pa.Int, Check.in_range(1, 120), nullable=True),
    "sex": Column(pa.Int, Check.isin([0, 1]), nullable=True),
    "cp": Column(pa.Int, Check.isin([1, 2, 3, 4]), nullable=True),
    "trestbps": Column(pa.Int, Check.in_range(10, 300), nullable=True),
    "chol": Column(pa.Int, Check.in_range(100, 600), nullable=True),
    "fbs": Column(pa.Int, Check.isin([0, 1]), nullable=True),
    "restecg": Column(pa.Int, Check.isin([0, 1, 2]), nullable=True),
    "thalach": Column(pa.Int, Check.in_range(50, 250), nullable=True),
    "exang": Column(pa.Int, Check.isin([0, 1]), nullable=True),
    "oldpeak": Column(pa.Float, Check.ge(0.0), nullable=True),
    "slope": Column(pa.Int, Check.isin([1, 2, 3]), nullable=True),
    "ca": Column(pa.Float, Check.isin([0, 1, 2, 3]), nullable=True),
    "thal": Column(pa.Float, Check.isin([3, 6, 7]), nullable=True),
    "num": Column(pa.Int, Check.isin([0, 1, 2, 3, 4])),
})
