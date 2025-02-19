

class QualityType:
    def __init__(self, type_name):
        self.type = type_name


    def __str__(self):
        return f'Quality ({self.type} Modifiers)'

    def __repr__(self):
        return f'{self.type} Quality Type'



class DefaultQuality(QualityType):
    def __init__(self):
        super().__init__('Default')

    def __str__(self):
        return 'Quality'


ATTACK_QUALITY = QualityType('Attack')
PHYSICAL_QUALITY = QualityType('Physical')
LIGHTNING_QUALITY = QualityType('Lightning')
FIRE_QUALITY = QualityType('Fire')
COLD_QUALITY = QualityType('Cold')
CHAOS_QUALITY = QualityType('Chaos')
MANA_QUALITY = QualityType('Mana')
LIFE_QUALITY = QualityType('Life')
DEFENCE_QUALITY = QualityType('Defence')
ATTRIBUTE_QUALITY = QualityType('Attribute')
SPEED_QUALITY = QualityType('Speed')
DEFAULT_QUALITY = DefaultQuality()
