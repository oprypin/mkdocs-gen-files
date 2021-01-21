import mkdocs_gen_files

for total in range(19, 100, 20):
    with mkdocs_gen_files.open(f"sample/{total}-bottles.md", "w") as f:
        for i in reversed(range(1, total + 1)):
            print(f"{i} bottles of beer on the wall, {i} bottles of beer  ", file=f)
            print(f"Take one down and pass it around, **{i-1}** bottles of beer on the wall\n", file=f)
