#!/bin/bash
if [ -z "$FG_ROOT" ]; then
    echo "Please, define FG_ROOT"
    exit 1
fi

REGIONS_DIR="$FG_ROOT/Materials/regions"

python3 plot_regions.py -v -o regions "$REGIONS_DIR"
python3 plot_regions.py -v --single -o . "$REGIONS_DIR"

cat materials.txt | while read MATERIAL; do
    python3 plot_regions.py -v -o materials --single --material "$MATERIAL" --alpha 1 --edgecolor gray --legend "$REGIONS_DIR"
done

python3 plot_regions.py -v --legend --single -o examples "$REGIONS_DIR"
python3 plot_regions.py --single -a 1 --legend --material IrrCrop --output materials --edgecolor gray --boundaries '[-30, 45, 30, 70]' $FG_ROOT/Materials/regions
