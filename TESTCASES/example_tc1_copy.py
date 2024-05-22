from . import example_tc1_direct


class TestCase123(example_tc1_direct.TestCase):
    DESCRIPTION = "copy1"

    def run__wrapped(self) -> bool:
        self.details_update({"index": self.DEVICES.DUT.INDEX})
        return super().run__wrapped()
