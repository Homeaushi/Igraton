from random import random


class EnemyAI:
    def update(self, enemy, player):
        # Простая логика преследования
        if enemy.rect.x < player.rect.x:
            enemy.move_right()
        else:
            enemy.move_left()

        # Случайные атаки
        if random.random() < 0.01:
            enemy.attack_up()
