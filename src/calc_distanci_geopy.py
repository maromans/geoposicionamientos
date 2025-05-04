from geopy.distance import distance

coord1 = (-34.6037, -58.3816)  # Buenos Aires
coord2 = (-32.9587, -60.6939)  # Rosario

distancia_km = distance(coord1, coord2).km
print(f"La distancia es de {distancia_km:.2f} km")

