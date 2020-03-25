from pycroaktools.presentation.presentation import Presentation
from pycroaktools.presentation.slides import Slides
from pycroaktools.presentation.slide import Slide
from pycroaktools.workflow.workflow import Workflow
from pycroaktools.presentation.images import Images
import os
import re
import logging


class WorkflowToPresentation:
    """
    The WorkflowToPresentation class builds a bridge between a defined workflow and a presentation.
    It generates presentations starting from this workflow and by matching Workflow data and Slides data.
    These presentations are versioned. The content evolve easily by requesting slide versions corresponding 
    to the expected presentation version.

    To do so, 2 functions are available : 
    - createLinearPresentations : each possible path defined by the workflow generates an individual presentation. 
    Then Each slide has only one next slide. This is a linear sequence from first to last slide.

    - createWorkflowPresentation: a unique presentation is generated to represent the workflow. Each slide may has multiple next slides. 
    Then links give choices to follow a path or another in the workflow

    """

    def __init__(self, workflow: Workflow, slides: Slides, outputFolder):
        """
        Builds the object
        ---
        Parameters:
        - workflow: workflow definition
        - slides: slides that should match the workflow
        - outputFolder: folder where the presentations are saved

        """
        self.workflow = workflow
        self.slides = slides
        self.outputFolder = outputFolder

    def _getPresNames(self, paths, version):
        presNames = []
        for path in paths:
            presName = self.workflow.name+'_v'+str(version)+'_'
            for step in path:
                presName += str(step.id)+'-'
            presNames.append(presName[:-1]+'.html')
        return presNames

    def createLinearPresentations(self, version):
        """
        Each possible path defined by the workflow generates an individual presentation. 
        Then Each slide has only one next slide. This is a linear sequence from first to last slide.
        ---
        Parameters:
        - version: expected version of the presentation. Then this version of the slides is searched and if not
        found the previous one is used.
        """
        paths = self.workflow.getAllPaths()
        presNames = self._getPresNames(paths, version)

        for index, path in enumerate(paths):
            slideIds = [step.id for step in path]
            Presentation().createPresentation(
                presNames[index], self.slides, slideIds, self.outputFolder, version=version)

    def createWorkflowPresentation(self, version):
        """
        A unique presentation is generated to represent the workflow. Each slide may has multiple next slides. 
        Then links give choices to follow a path or another in the workflow
        ---
        Parameters:
        - version: expected version of the presentation. Then this version of the slides is searched and if not
        found the previous one is used.
        """
        presName = self.workflow.name + '_v' + str(version)+'.html'
        slideIds = [step.id for step in self.workflow.getSteps()]
        links = self.workflow.getLinksPerSteps()

        Presentation().createPresentation(presName, self.slides, slideIds, self.outputFolder,
                                          links, version)
