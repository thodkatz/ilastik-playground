from ilastik.lazyflow.graph import Operator, InputSlot, OutputSlot, Graph
from ilastik.lazyflow.stype import ArrayLike
import numpy as np
from ilastik.examples.opSimplePixelClassification import OpSimplePixelClassification

def test_propagate_dirty():
    class SumOperator(Operator):
        input1 = InputSlot()
        input2 = InputSlot()
        output = OutputSlot()
        
        def execute(self, slot, subindex, roi, result):
            a = self.input1.get(roi).wait()
            b = self.input2.get(roi).wait()
            
            result[...] = a+b
            
        def setupOutputs(self):
            shapeA = self.input1.meta.shape
            shapeB = self.input2.meta.shape
            
            self.output.meta.shape = shapeA
            self.output.meta.dtype = self.input1.meta.dtype
            
        def propagateDirty(self, slot, subindex, roi):
            self.output.setDirty(roi)
            
            
    graph = Graph()
            
    op = SumOperator(graph=graph)
    op.output.notifyDirty(lambda *args: print("I got dirty 1"))
    op.input1.setValue(np.zeros((2, 2)))
    op.input2.setValue(np.ones((2, 2)))
    out = op.output[:].wait() # [[1, 1], [1, 1]]
    print(out)
    
    
    
    op.input2
    op.output
    
    
    op.input1.setValue(np.ones((2, 2)))
    
    # value has been updated to [[2, 2, ], [2, 2]] although propagate dirty hasn't mapped how input changes propage to output
    print(op.output.value)



test_propagate_dirty()


