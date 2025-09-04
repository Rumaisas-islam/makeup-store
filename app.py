import re
class MakeupWorld:
  def __init__(self,filename="record.txt"):
    self.filename=filename
  def create_backup(self):
    import shutil
    backup_file = self.filename.replace(".txt"," backup.txt")
    shutil.copy(self.filename,backup_file)
    print(f"Backup created as:{backup_file}")

  def add_product(self):
    print("Welcome to MakeupStore")
    while True:
      product=input("Enter product name: ").strip()
      if product.replace(" ","").isalpha():
        break
      else:
        print("Invalid input!Product should only contains alphabets")
    while True:
      price=input("Enter product price: ").strip()
      if price.isdigit():
        break
      else:
        print("Invalid input!Price should only contains numbers")
    while True:
      company=input("Enter product company: ").strip()
      if company.replace(" ","").isalpha():
        break
      else:
        print("Invalid input!Company should only contain alphabets")
    while True:
      use=input("Enter use of product: ").strip()
      if use.replace(" ","").isalpha():
        break
      else:
        print("Invalid input!Use should only contains alphabets")

    try:
      with open(self.filename,"a",encoding="UTF-8") as f:
        f.write(f"Product:{product}\n")
        f.write(f"Price:{price}\n")
        f.write(f"Company:{company}\n")
        f.write(f"Use:{use}\n")
        f.write("---------------------------\n")
    except Exception as e:
      print(f"Error saving:{e}")
  def search_product(self,field):
    try:
      with open(self.filename,"r",encoding="UTF-8") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    value=input(f"Enter the {field.lower()} to search product: ").strip()
    pattern = rf"(?i)^{re.escape(field)}:\s*{re.escape(value)}$"
    block=[]
    found=False
    for line in lines:
      if line.strip()== "---------------------------":
        if any(re.match(pattern, l.strip(), re.IGNORECASE) for l in block):
          print("\n".join(block))
          print("---------------------------")
          found=True
        block=[]
      else:
        block.append(line.strip())
    if block:
      if any(re.match(pattern, l.strip(), re.IGNORECASE) for l in block):
        print("\n".join(block))
        print("---------------------------")
        found=True
      block=[]
    if not found:
      print(f"No product found with that {field.lower()} name")
  def delete_product(self,field):
    try:
      with open(self.filename,"r",encoding="UTF-8") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No filefound")
      return
    value=input(f"Enter the {field.lower()} to delete product: ").strip()
    block,new_lines=[],[]
    pattern = rf"(?i)^{re.escape(field)}:\s*{re.escape(value)}$"
    found_any=False
    for line in lines:
      if line.strip()=="---------------------------":
        if any(re.match(pattern, l.strip(), re.IGNORECASE) for l in block):
          print("\n Matched Task Record:")
          print("\n".join(block))
          print("---------------------------")
          confirm=input("Do you want to delete this(yes/no): ").lower()
          if confirm == "yes":
            self.create_backup()
            found_any=True
          else:
            new_lines.extend(block+["---------------------------\n"])
        else:
          new_lines.extend(block+["---------------------------\n"])
        block=[]
      else:
        block.append(line)
    if found_any:
      with open(self.filename,"w",encoding="UTF-8") as f:
        f.writelines(new_lines)
      print("Selected product deleted")
    else:
      print(f"No product found with that {field.lower()} name")
  def edit_product(self,field):
    try:
      with open(self.filename,"r",encoding="UTF-8") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    value=input(f"Enter the {field.lower()} to edit product: ").strip()
    pattern = rf"(?i)^{re.escape(field)}:\s*{re.escape(value)}$"
    new_lines,block=[],[]
    found_any=False
    for line in lines:
      if line.strip()=="---------------------------":
        if any(re.match(pattern, l.strip(), re.IGNORECASE) for l in block):
          print("\n Matched Product Record:")
          print("\n".join(block))
          print("---------------------------")
          confirm=input("Are you sure you want to edit this product(yes/no): ")
          if confirm == "yes":
            self.create_backup()
            found_any=True
            while True:
              product=input("Enter product name: ").strip()
              if product.replace(" ","").isalpha():
                break
              else:
                print("Invalid input!Product should only contains alphabets")
            while True:
              price=input("Enter product price: ").strip()
              if price.isdigit():
                break
              else:
                print("Invalid input!Price should only contains numbers")
            while True:
              company=input("Enter product company: ").strip()
              if company.replace(" ","").isalpha():
                break
              else:
                print("Invalid input!Company should only contain alphabets")
            while True:
              use=input("Enter use of product: ").strip()
              if use.replace(" ","").isalpha():
                break
              else:
                print("Invalid input!Use should only contains alphabets")
            
            new_lines.append(f"Product:{product}\n")
            new_lines.append(f"Price:{price}\n")
            new_lines.append(f"Company:{company}\n")
            new_lines.append(f"Use:{use}\n")
            new_lines.append("---------------------------\n")
          else:
            new_lines.extend(block+ ["---------------------------\n"])
        else:
          new_lines.extend(block+ ["---------------------------\n"])
        block=[]
      else:
        block.append(line)
    if found_any:
      with open(self.filename,"w",encoding="UTF-8") as f:
        f.writelines(new_lines)
      print("Selected product updated successfully.")
    else:
      print(f"No product found with that {field.lower()} name")
  def list_product_names(self):
    try:
      with open(self.filename,"r",encoding="UTF-8") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    products= [line.strip().replace("Product:", "") for line in lines if line.startswith("Product:")]
    if products:
      print("All Product Names")
      for idx,product in enumerate(products,1):
        print(f"{idx}.{product}")
    else:
      print("No product found")
  def print_all_products(self):
    try:
      with open(self.filename,"r",encoding="UTF-8") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    block=[]
    task_num=1
    found=False
    for line in lines:
      if line.strip()=="---------------------------":
        if block:
          print(f"\nTask:{task_num}:")
          print("".join(block).strip())
          found=True
          task_num+=1
        block=[]
      else:
        block.append(line)
    if not found:
      print("No products found")
if __name__ == "__main__":
  obj=MakeupWorld()
  while True:
    print("\n1.Add product")
    print("2.Search product")
    print("3.Delete Product")
    print("4.Edit product")
    print("5.List all product names")
    print("6.List all products")
    print("7.Exit")
    choice=input("Enter your choice(1-7): ")
    if choice == '1':
      obj.add_product()
    elif choice == '2':
      field=input("Search by (Product/Company): ").strip().capitalize()
      if field in ["Product","Company"]:
        obj.search_product(field)
      else:
        print("Invalid input!Please enter Product or Company")
    elif choice == "3":
      field=input("Delete by (Product/Company): ").strip().capitalize()
      if field in ["Product" , "Company"]:
        obj.delete_product(field)
      else:
        print("Invalid input!Please enter Product or Company")
    elif choice == "4":
      field=input("Edit by (Product/Company): ").strip().capitalize()
      if field in ["Product" ,"Company"]:
        obj.edit_product(field)
      else:
        print("Invalid input!Please enter Product or Company")
    elif choice == "5":
      obj.list_product_names()
    elif choice == "6":
      obj.print_all_products()
    elif choice == "7":
      print("Exiting Makeup world. Goodbye!")
      break
    else:
      print("Invalid input!Try again")
