# nsm_code_base


# 📘 **Usage: osi_layer3_ping_of_death_attack.py**

```
python3 osi_layer3_ping_of_death_attack.py [options]
```

## **Options**

### **--roster <file>**
Path to the roster JSON file.  
If not provided, the script defaults to:

```
ids_sec3_students.json
```

Example:

```
--roster ids_sec4_students.json
```

---

### **--target-group <groupname>**
Attack every IP inside the specified group.

Example:

```
--target-group group1
```

---

### **--target-ip <ip>**
Attack a single IP address.

Example:

```
--target-ip 192.150.84.81
```

---

## **Examples**

### **Attack a whole group from a specific roster**
```
python3 osi_layer3_ping_of_death_attack.py \
    --roster ids_sec4_students.json \
    --target-group group2
```

### **Attack a single student**
```
python3 osi_layer3_ping_of_death_attack.py \
    --roster ids_sec4_students.json \
    --target-ip 192.150.84.81
```

### **Use the default roster**
```
python3 osi_layer3_ping_of_death_attack.py --target-group group1
```

---

If you want, I can also generate a **short version** for the top of the file or a **student‑friendly version** for Canvas.