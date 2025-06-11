import json
import os
import typing

class Information(typing.TypedDict):
	hash: str
	size: int

mpath: str = input("Where is minecraft located? ")
if not os.path.isdir(mpath):
	raise ValueError("Liar liar, pants on fire!")
vers: str = input("What index of objects should I search? ")
if not os.path.isfile(f"{mpath}/assets/indexes/{vers}.json"):
	raise ValueError("Liar liar, pants on fire!")
loc: str = input("Where do you want me to put it? ")
if os.path.dirname(loc) and not os.path.isdir(os.path.dirname(loc)):
	raise ValueError("Liar liar, pants on fire!")

with open(f"{mpath}/assets/indexes/{vers}.json") as f:
	try:
		index: dict[typing.Literal["objects"], dict[str, Information]] = json.load(f)
	except json.JSONDecodeError:
		raise ValueError("Uh-Oh. The index is invalid json.")
	
	if not ("objects" in index and isinstance(index["objects"], dict)):
		raise ValueError("Uh-Oh. The index doesn't have the objects.")
	
	if len(index) > 1:
		if input('The index has keys other than "objects". Ignore? ')[0].lower() == "y":
			print("Ignored.")
		else:
			raise ValueError('This index has keys other than "objects".')

ignore_non_dicts: bool = False
ignore_missing_hash: bool = False
ignore_missing_size: bool = False
ignore_too_many_keys: bool = False
ignore_missing_path: bool = False
ignore_size_mismatch: bool = False
for name, ind in index["objects"].items():
	if not isinstance(ind, dict):
		if ignore_non_dicts:
			print(f"Object ({name}) not object. Ignored.")
			continue
		if input(f"This object ({name}) is not an object. Ignore? ")[0].lower() == "y":
			ignore_non_dicts = True
			print("Ignored.")
			continue
		raise ValueError("This object is not an object.")
	if not ("hash" in ind and isinstance(ind["hash"], str)):
		if ignore_missing_hash:
			print(f"Hash missing ({name}). Ignored.")
			continue
		if input(f"This object ({name}) is missing a hash. Ignore? ")[0].lower() == "y":
			ignore_missing_hash = True
			print("Ignored.")
			continue
		raise ValueError("This object is missing a hash.")
	if not ("hash" in ind and isinstance(ind["hash"], str)):
		if ignore_missing_hash:
			print(f"Hash missing ({name}). Ignored.")
			continue
		if input(f"This object ({name}) is missing a hash. Ignore? ")[0].lower() == "y":
			ignore_missing_hash = True
			print("Ignored.")
			continue
		raise ValueError("This object is missing a hash.")
	if not ("size" in ind and isinstance(ind["size"], int)):
		if ignore_missing_size:
			print(f"Size missing ({name}). Ignored.")
		elif input(f"This object ({name}) is missing a size. Ignore? ")[0].lower() == "y":
			ignore_missing_size = True
			print("Ignored.")
		else:
			raise ValueError("This object is missing a hash.")
	if len(ind) > ("size" in ind) + 1:
		if ignore_too_many_keys:
			print(f"Too many keys ({name}). Ignored.")
		elif input(f"This object ({name}) has too many keys. Ignore? ")[0].lower() == "y":
			ignore_too_many_keys = True
			print("Ignored.")
		else:
			raise ValueError("This object has too many keys.")
	if not os.path.isfile(f"{mpath}/assets/objects/{ind["hash"][:2]}/{ind["hash"]}"):
		if ignore_missing_path:
			print(f"Object ({name}) not found at path {mpath}/assets/objects/{ind["hash"][:2]}/{ind["hash"]}. Ignored.")
		elif input(f"This object ({name}) can't be found at {mpath}/assets/objects/{ind["hash"][:2]}/{ind["hash"]}. Ignore? ")[0].lower() == "y":
			ignore_missing_path = True
			print("Ignored.")
		else:
			raise ValueError("This object can't be found.")
	with open(f"{mpath}/assets/objects/{ind["hash"][:2]}/{ind["hash"]}", "rb") as fb:
		data: bytes = fb.read()
	if ("size" in ind and isinstance(ind["size"], int)) and len(data) != ind["size"]:
		if ignore_size_mismatch:
			print(f"Length of object ({name}) not matching with size ({ind["size"]}). Ignored.")
		elif input(f"This object ({name}) doesn't have size {ind["size"]}. Ignore? ")[0].lower() == "y":
			ignore_size_mismatch = True
			print("Ignored.")
		else:
			raise ValueError("This object has the wrong size.")
	if name == "pack.mcmeta":
		path: str = f"{loc}/{vers}/pack.mcmeta"
	else:
		path: str = f"{loc}/{vers}/assets/{name}"
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, "wb") as fb:
		fb.write(data)