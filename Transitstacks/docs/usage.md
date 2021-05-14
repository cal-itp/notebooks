# Typical Usage

## Browse Components in all Transit Stacks

```python
import transitstacks as ts
all_stacks = ts.Stack(
    ts.read_stack_from_gsheets(filter_dict = {"Transit Provider": "GET Bus"})
    )

# list all products
my_stack.components_df.products

# get most common products
my_stack.components_df['products'].value_counts().sort_values(as‌​cending=False)
```

## Browse relationships in Single Transit Stack

```python
import transitstacks as ts
my_stack = ts.Stack(
    ts.read_stack_from_gsheets(filter_dict = {"Transit Provider": "GET Bus"})
    )

my_stack.relationships_df
```

## Create a transit stack diagram with two grouping levels

```python
LEVEL1 = "Function Group"
LEVEL2 = "Product"

d = ts.stack_diagram(
    my_stack,
    cluster_level_1 = LEVEL1,
    cluster_level_2 = LEVEL2,
    bgcolor_cluster_L1 = ts.stack.greenyellow_functiongroup_map,
)

```

## Leveraging Jupyter Notebooks

Interactive dataframes in Jupyter Notebooks make it easier to explore the data in an ad-hoc manner.  Please refer to the following jupyter notebooks in the `/notebooks` directory as starting points:

- `Stack Database Analysis.ipynb`
- `Individual Transit Provider Analysis.ipynb`

 Jupyter notebooks can be started by activating the lasso conda environment and typing `jupyter notebook`:

 `conda activate <my_conda_environment>`   
 `jupyter notebook`  
