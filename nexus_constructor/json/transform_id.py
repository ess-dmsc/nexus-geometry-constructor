import attr


# frozen=True makes objects hashable (for use as dictionary key)
@attr.s(frozen=True)
class TransformId:
    """
    Uniquely identifies a Transformation
    """

    component_name = attr.ib(type=str)
    transform_name = attr.ib(type=str)
