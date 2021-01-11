from nio.block.mixins.enrich.enrich_signals import EnrichSignals
from nio.properties import VersionProperty
from .tuya_base import TuYaBase, TuYaDevice
import time


class TuYaInsight(TuYaBase, EnrichSignals):

    version = VersionProperty("0.1.1")

    def execute_tuya_command(self, signal):
        return_signal = None
        if not self._updating:
            self.logger.debug('Reading values from {} {}...'.format(
                self.ip, self.mac))
            self._updating = True
            try:
                if self.device.tuya is None:
                    return None
                return_signal = self.device.status()
                self._updating = False
            except:
                # raises when update_insight_params has given up retrying
                self.logger.error(
                     'Unable to connect to TuYa, dropping signal {}'.format(
                         signal))
                self.device = None
                self._updating = False
                return 
        else:
            # drop new signals while retrying
            self.logger.error(
                    'Another thread is waiting for param update, '
                    'dropping signal {}'.format(signal))
            return

        return return_signal


    def is_valid_device(self, device):
        return super().is_valid_device(device)
