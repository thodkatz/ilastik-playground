import vigra
from ilastik.lazyflow.classifiers.parallelVigraRfLazyflowClassifier import ParallelVigraRfLazyflowClassifierFactory
from ilastik.lazyflow.graph import Operator, InputSlot, OutputSlot, Graph
from ilastik.lazyflow.stype import ArrayLike
import numpy as np
from ilastik.examples.opSimplePixelClassification import OpSimplePixelClassification


features = np.indices((100, 100)).astype(np.float32) + 0.5
features = np.rollaxis(features, 0, 3)
features = vigra.taggedView(features, "yxc")
assert features.shape == (100, 100, 2)

# Define a couple arbitrary labels.
labels = np.zeros((100, 100, 1), dtype=np.uint8)
labels = vigra.taggedView(labels, "yxc")

labels[10, 10] = 1
labels[10, 11] = 1
labels[20, 20] = 2
labels[20, 21] = 2

graph = Graph()
opPixelClassification = OpSimplePixelClassification(graph=Graph())

# Specify the classifier type: A random forest with just 10 trees.
opPixelClassification.ClassifierFactory.setValue(ParallelVigraRfLazyflowClassifierFactory(10))

# In a typical use-case, the inputs to our operator would be connected to some upstream pipeline via Slot.connect().
# But for this test, we will provide the data as raw VigraArrays via the special Slot.setValue() function.
# Also, we have to manually resize() the level-1 slots.
opPixelClassification.Features.resize(1)
opPixelClassification.Features[0].setValue(features)

opPixelClassification.Labels.resize(1)
opPixelClassification.Labels.setValue(labels)

# Load the label cache, which will pull from the Labels slot...
print("Ingesting labels...")
opPixelClassification.ingest_labels()

print("Initiating prediction...")
predictions = opPixelClassification.Predictions[0][:].wait()
assert predictions.shape == (100, 100, 2)
assert predictions.dtype == numpy.float32
assert 0.0 <= predictions.min() <= predictions.max() <= 1.0
print("Done predicting.")