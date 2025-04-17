import os
import subprocess

from amaranth import *
from amaranth.build import *
from amaranth.vendor import GowinPlatform

from .resources import *


__all__ = ["TangPrimer20kPlatform"]


class TangPrimer20kPlatform(GowinPlatform):
    part          = "GW2A-LV18PG256C8/I7"
    family        = "GW2A-18"
    default_clk   = "clk27"
    resources     = [
        Resource("clk27", 0, Pins("H11", dir="i"),
                 Clock(27e6), Attrs(IO_TYPE="LVCMOS33")),


        *LEDResources(pins="L16 L14 N14 N16", invert=True,
                      attrs=Attrs(IO_TYPE="LVCMOS33")),

    ]
    connectors = []

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "add_options":
                "set_option -use_mspi_as_gpio 1 -use_sspi_as_gpio 1",
            "gowin_pack_opts":
                "--sspi_as_gpio --mspi_as_gpio"
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name):
        with products.extract("{}.fs".format(name)) as bitstream_filename:
            subprocess.check_call(["openFPGALoader", "-b", "tangprimer20k", bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    TangNano9kPlatform().build(Blinky(), do_program=True)
