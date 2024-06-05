import psycopg2


def get_weapons_with_types(keyword):
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cur = conn.cursor()

    query = """
    SELECT w.weapon_name, wt.type_name
    FROM weapons w
    JOIN weapon_types wt ON w.weapon_type_id = wt.type_id
    WHERE w.weapon_name LIKE %s OR wt.type_name LIKE %s;
    """
    cur.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))

    results = cur.fetchall()
    cur.close()
    conn.close()

    return results


weapons_with_types = get_weapons_with_types("keyword")
for weapon in weapons_with_types:
    print(weapon)
#-------------------
def get_vehicles_with_types(keyword):
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cur = conn.cursor()

    query = """
    SELECT v.vehicle_name, vt.type_name
    FROM vehicles v
    JOIN vehicle_types vt ON v.vehicle_type_id = vt.type_id
    WHERE v.vehicle_name LIKE %s OR vt.type_name LIKE %s;
    """
    cur.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))

    results = cur.fetchall()
    cur.close()
    conn.close()

    return results


vehicles_with_types = get_vehicles_with_types("keyword")
for vehicle in vehicles_with_types:
    print(vehicle)
#-----------------------------------------------------
def get_weapons_with_soldiers(keyword):
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cur = conn.cursor()

    query = """
    SELECT w.weapon_name, s.soldier_type
    FROM weapons w
    JOIN soldiers s ON w.weapon_id = s.primary_weapon_id
    WHERE w.weapon_name LIKE %s OR s.soldier_type LIKE %s;
    """
    cur.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))

    results = cur.fetchall()
    cur.close()
    conn.close()

    return results


weapons_with_soldiers = get_weapons_with_soldiers("keyword")
for weapon in weapons_with_soldiers:
    print(weapon)
#------------------------------------------------------
def get_weapon_types_with_soldiers(keyword):
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cur = conn.cursor()

    query = """
    SELECT wt.type_name, s.soldier_type
    FROM weapon_types wt
    JOIN weapons w ON wt.type_id = w.weapon_type_id
    JOIN soldiers s ON w.weapon_id = s.primary_weapon_id
    WHERE wt.type_name LIKE %s OR s.soldier_type LIKE %s;
    """
    cur.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))

    results = cur.fetchall()
    cur.close()
    conn.close()

    return results


weapon_types_with_soldiers = get_weapon_types_with_soldiers("keyword")
for weapon_type in weapon_types_with_soldiers:
    print(weapon_type)
#----------------------------------------------------------------
#
#
#
def main(keyword):
    print("Weapons with Types:")
    weapons_with_types = get_weapons_with_types(keyword)
    for weapon in weapons_with_types:
        print(weapon)

    print("\nVehicles with Types:")
    vehicles_with_types = get_vehicles_with_types(keyword)
    for vehicle in vehicles_with_types:
        print(vehicle)

    print("\nWeapons with Soldiers:")
    weapons_with_soldiers = get_weapons_with_soldiers(keyword)
    for weapon in weapons_with_soldiers:
        print(weapon)

    print("\nWeapon Types with Soldiers:")
    weapon_types_with_soldiers = get_weapon_types_with_soldiers(keyword)
    for weapon_type in weapon_types_with_soldiers:
        print(weapon_type)

if __name__ == "__main__":
    keyword = "your_search_keyword"
    main(keyword)
