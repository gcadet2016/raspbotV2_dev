# Command syntaxes

## Collect calibration images
Settings configured in settings.conf

```
cd stereoVision
python main.py -cmd capture
```

## Calibrate stereo Camera
Settings configured in settings.conf

```
cd stereoVision
python main.py -cmd calibrate
```

## Display epipolar lines
```
cd stereoVision
python main.py -cmd epipolar
```

# To be tested

## epilolar
*python main.py -cmd epipolar* n'affiche qu'une fenêtre lors de première exécution

Sur rapberryPi: tester la capture d'image pour le tracé des épipolar lines
```
cd stereoVision
python main.py -cmd epipolar -c
```
