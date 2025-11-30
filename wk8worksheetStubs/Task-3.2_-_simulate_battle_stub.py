"""
Exercise 3.2: Simulate a Turn-Based Battle (Class-Based)

In this exercise, you will create a Pokemon class and use it to simulate battles.
This demonstrates object-oriented programming principles: encapsulation, methods, and clear responsibilities.
"""

import httpx


class Pokemon:
    """
    Represents a Pokemon with stats fetched from the PokeAPI.
    """

    def __init__(self, name):
        """
        Initialise a Pokemon by fetching its data from the API and calculating its stats.
        """
        # Store the name (formatted nicely)
        self.name = name.capitalize()

        # Fetch Pokémon data from API
        url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        response = httpx.get(url)

        if response.status_code != 200:
            raise ValueError(f"Pokémon '{name}' not found!")

        data = response.json()

        # Extract base stats
        base_stats = {}
        for block in data["stats"]:
            stat_name = block["stat"]["name"]
            base_stats[stat_name] = block["base_stat"]

        # Calculate final stats
        self.stats = {
            "attack": self._calculate_stat(base_stats["attack"]),
            "defense": self._calculate_stat(base_stats["defense"]),
            "speed": self._calculate_stat(base_stats["speed"]),
            "hp": self._calculate_hp(base_stats["hp"])
        }

        # HP variables
        self.max_hp = self.stats["hp"]
        self.current_hp = self.max_hp

    def _calculate_stat(self, base_stat, level=50, iv=15, ev=85):
        """
        Calculate a Pokemon's attack/defense/speed stat.
        Formula: int(((2*base + iv + ev/4) * level / 100) + 5)
        """
        return int(((2 * base_stat + iv + (ev / 4)) * level / 100) + 5)

    def _calculate_hp(self, base_stat, level=50, iv=15, ev=85):
        """
        Calculate a Pokemon's HP.
        Formula: int(((2*base + iv + ev/4) * level / 100) + level + 10)
        """
        return int(((2 * base_stat + iv + (ev / 4)) * level / 100) + level + 10)

    def attack(self, defender):
        """
        Attack another Pokemon and return the damage dealt.
        """
        level = 50
        base_power = 60

        damage = int(
            (((2 * level * 0.4 + 2) * self.stats["attack"] * base_power)
             / (defender.stats["defense"] * 50)) + 2
        )

        defender.take_damage(damage)
        return damage

    def take_damage(self, amount):
        """
        Reduce HP by damage, preventing negative HP.
        """
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0

    def is_fainted(self):
        """
        Returns True if Pokémon has fainted (HP <= 0).
        """
        return self.current_hp <= 0

    def __str__(self):
        """
        Output format: Pikachu (HP: 87/120)
        """
        return f"{self.name} (HP: {self.current_hp}/{self.max_hp})"


def simulate_battle(pokemon1_name, pokemon2_name):
    """
    Simulate a turn-based Pokémon battle.
    """
    # Create Pokémon objects
    p1 = Pokemon(pokemon1_name)
    p2 = Pokemon(pokemon2_name)

    print("\n--- Pokémon Battle ---")
    print(p1)
    print(p2)
    print("----------------------\n")

    # Determine who attacks first
    if p1.stats["speed"] > p2.stats["speed"]:
        attacker, defender = p1, p2
    elif p2.stats["speed"] > p1.stats["speed"]:
        attacker, defender = p2, p1
    else:
        attacker, defender = p1, p2  # default

    print(f"{attacker.name} attacks first!\n")

    round_num = 1
    while not attacker.is_fainted() and not defender.is_fainted():
        print(f"--- Round {round_num} ---")
        damage = attacker.attack(defender)
        print(f"{attacker.name} deals {damage} damage!")
        print(defender)

        if defender.is_fainted():
            print(f"\n{defender.name} fainted!")
            break

        # swap attacker and defender
        attacker, defender = defender, attacker
        round_num += 1

    print("\n--- Battle Over ---")
    print(f"Winner: {attacker.name} with {attacker.current_hp} HP left\n")


if __name__ == "__main__":
    simulate_battle("pikachu", "bulbasaur")
