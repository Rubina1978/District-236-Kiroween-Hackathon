from .spider_obj import Spider
from ..animator_controller import animator_interface


class PoolingSystem:

    def __init__(self, pool_size=10):

        self.deactivated = [
            Spider(animator=animator_interface("spider"))
            for _ in range(pool_size)
        ]

        self.activated = []

    def check_dead(self):
        """Return dead spiders to the inactive pool."""

        for spider in self.activated[:]:

            if spider.is_dead:

                self.activated.remove(spider)
                self.deactivated.append(spider)

    def respawn_spider(self, position):

        if not self.deactivated:
            return None

        spider = self.deactivated.pop()

        spider.reset(position)

        self.activated.append(spider)

        return spider

    def get_activated_enemies(self):

        return self.activated