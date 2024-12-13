import numpy as np

def fuzzify_luas(luas):
    sempit = max(0, min((11 - luas) / 3, 1))
    sedang = max(0, min((luas - 10) / 1, (13 - luas) / 3))
    luas = max(0, min((luas - 12) / 5, 1))
    return sempit, sedang, luas

def fuzzify_jarak(jarak):
    dekat = max(0, min((1300 - jarak) / 400, 1))
    sedang = max(0, min((jarak - 1200) / 500, (1700 - jarak) / 500))
    jauh = max(0, min((jarak - 1600) / 600, 1))
    return dekat, sedang, jauh


def fuzzify_fasilitas(fasilitas):
    # Fuzzy logic for "biasa" (range 0-20)
    biasa = max(0, min((20 - fasilitas) / 20, 1)) if fasilitas <= 20 else 0

    # Fuzzy logic for "lengkap" (range 15-31)
    lengkap = max(0, min((fasilitas - 15) / 16, 1)) if fasilitas >= 15 else 0

    return biasa, lengkap


def mamdani(luas, jarak, fasilitas):
    luas_membership = fuzzify_luas(luas)
    jarak_membership = fuzzify_jarak(jarak)
    fasilitas_membership = fuzzify_fasilitas(fasilitas)

    # Define rules
    rules = [
        ("Murah", min(jarak_membership[0], luas_membership[0], fasilitas_membership[0])),  # Rule 1
        ("Murah", min(jarak_membership[0], luas_membership[1], fasilitas_membership[0])),  # Rule 2
        ("Murah", min(jarak_membership[0], luas_membership[2], fasilitas_membership[0])),  # Rule 3
        ("Murah", min(jarak_membership[1], luas_membership[0], fasilitas_membership[0])),  # Rule 4
        ("Murah", min(jarak_membership[1], luas_membership[1], fasilitas_membership[0])),  # Rule 5
        ("Murah", min(jarak_membership[1], luas_membership[2], fasilitas_membership[0])),  # Rule 6
        ("Murah", min(jarak_membership[2], luas_membership[0], fasilitas_membership[0])),  # Rule 7
        ("Murah", min(jarak_membership[2], luas_membership[1], fasilitas_membership[0])),  # Rule 8
        ("Murah", min(jarak_membership[2], luas_membership[2], fasilitas_membership[0])),  # Rule 9
        ("Mahal", min(jarak_membership[0], luas_membership[0], fasilitas_membership[1])),  # Rule 10
        ("Mahal", min(jarak_membership[0], luas_membership[1], fasilitas_membership[1])),  # Rule 11
        ("Mahal", min(jarak_membership[0], luas_membership[2], fasilitas_membership[1])),  # Rule 12
        ("Mahal", min(jarak_membership[1], luas_membership[0], fasilitas_membership[1])),  # Rule 13
        ("Mahal", min(jarak_membership[1], luas_membership[1], fasilitas_membership[1])),  # Rule 14
        ("Mahal", min(jarak_membership[1], luas_membership[2], fasilitas_membership[1])),  # Rule 15
        ("Mahal", min(jarak_membership[2], luas_membership[0], fasilitas_membership[1])),  # Rule 16
        ("Mahal", min(jarak_membership[2], luas_membership[1], fasilitas_membership[1])),  # Rule 17
        ("Mahal", min(jarak_membership[2], luas_membership[2], fasilitas_membership[1])),  # Rule 18
    ]

    # Aggregation of rules
    murah_membership = max(weight for label, weight in rules if label == "Murah")
    mahal_membership = max(weight for label, weight in rules if label == "Mahal")

    # Defining output fuzzy sets
    harga_range = np.linspace(500000, 1600000, 1000)
    murah_set = np.maximum(0, np.minimum(1, (800000 - harga_range) / 300000))
    mahal_set = np.maximum(0, np.minimum(1, (harga_range - 700000) / 900000))

    # Apply rule strengths to the fuzzy sets
    aggregated_set = np.maximum(
        np.minimum(murah_membership, murah_set),
        np.minimum(mahal_membership, mahal_set)
    )

    # Defuzzification using centroid method
    defuzzified_value = np.sum(aggregated_set * harga_range) / np.sum(aggregated_set)
    return defuzzified_value

# Example usage
luas = 12
jarak = 1200
fasilitas = 10
harga = mamdani(luas, jarak, fasilitas)
print(f"Harga kos-kosan adalah: Rp {harga:.0f}")
