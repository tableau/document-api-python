

class BaseObject:

    def _to_dict(
        self, base_attrs=[], to_dict_attrs=[],
        to_dict_list_attrs=[], to_dict_of_dict_attrs=[]
    ):
        base =  {
            k.replace('_', ''): getattr(self, k) for k in base_attrs
            if getattr(self, k)
        }
        base.update(
            {
                k: getattr(self, k).to_dict() for k in to_dict_attrs
                if getattr(self, k)
            }
        )
        base.update(
            {
                k: [i.to_dict() for i in getattr(self, k)]
                for k in to_dict_list_attrs
                if getattr(self, k)
            }
        )
        base.update(
            {
                i: {k:v.to_dict() for k, v in getattr(self, i).items()}
                for i in to_dict_of_dict_attrs
                if getattr(self, i)
            }
        )
        return base
