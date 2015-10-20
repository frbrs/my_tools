class MyComp(nukescripts.PythonPanel):
    """"Creates an UI to load passes, creates a hierarchy, and apply given parameters to Read and Write nodes """
    def __init__( self ):
        nukescripts.PythonPanel.__init__( self, "Parameters")


        #Create knobs name and types
        self.file = nuke.File_Knob('lighting', 'Lighting Passe Path:')
        self.start = nuke.Int_Knob( "start", "Start Frame:" )
        self.end = nuke.Int_Knob( "end", "End Frame:" )
        self.frameR = nuke.Boolean_Knob("frameR", "Don't set Frame Range")        
        self.fps = nuke.Double_Knob( "fps", "FPS:" )
        self.postageS = nuke.Boolean_Knob("postageS", "postage stamp")
        self.projectP = nuke.Boolean_Knob("projectP", "Apply options to Project?")
        self.format = nuke.Format_Knob("format","Format:")
        self.missing = nuke.Enumeration_Knob("missing_frames","Missing frames:",['error','black','checkerboard','nearest frame'])
        self.colorspace = nuke.Enumeration_Knob("colorspace","Colorspace :",['default(sRGB)','linear','Gamma1.8','Gamma2.2'])
        self.passes = nuke.Multiline_Eval_String_Knob("passes",'Other Passes:')
        self.setMinimumSize(600,400)
        self.before = nuke.Enumeration_Knob("","",["hold","loop","bounce","black"])
        self.after = nuke.Enumeration_Knob("","",["hold","loop","bounce","black"])
        self.occlu = nuke.File_Knob('occlusion', 'Occlusion Passe Path:')

        #Set Values
        self.passes.setValue("GlobalIllumination\nReflection\nSpecular\nRefraction\nSSS2")   
        self.projectP.setValue(True)
        self.fps.setRange(0,50)
        self.postageS.setValue(True)

        #Add Knobs
        for k in (self.file, self.passes,  self.occlu, self.start, self.before, self.end, self.frameR, self.postageS,self.after, self.fps ,self.format, self.missing, self.colorspace, self.projectP):
            self.addKnob(k)

    def master_read(self):
        """ Creates the first passe"""
        seqpath = self.file.value()

        #Check Sequence
        exr = ".exr"; tiff = ".tif"
        if (exr in seqpath) or (tiff in seqpath) :
            existingMasterR = []
            existing="MasterRead"
            
            #Operations on file name
            self.filePath = seqpath
            self.dirFile = self.filePath.split(".VRay")
            self.dirFile = self.dirFile[0]
            self.extension = self.filePath.split(".")
            self.extension = self.extension[-1]


            #If a MasterRead exists
            for n in nuke.allNodes('Read'):
               if existing in n.name()  :
                   existingMasterR.append(n.name())
            
            if existingMasterR == []:
                self.masterR = nuke.createNode("Read")
                self.masterR['name'].setValue("MasterRead")
                self.masterR['file'].setValue(self.filePath)
            else:
                nameValue = len(existingMasterR)
                nameValue+=1
                nameValue=  str(nameValue)

                self.masterR = nuke.createNode("Read")
                self.masterR['name'].setValue("MasterRead"+ nameValue)
                self.masterR['file'].setValue(self.filePath)
        else:
            nuke.message('Please select a correct sequence!')
            return self.create_hierarchy()
            
    def modify_nodes(self):
        """ applies given parameters to read and write Nodes """
		
        nformat = self.format.value()
        nstart = self.start.value()
        nend = self.end.value()
        nmissing = self.missing.value()
        ncolorspace = self.colorspace.value()
        nbefore = self.before.value()
        nafter = self.after.value()
        
        # Read Nodes
        for n in nuke.allNodes('Read'):
        
            # Check frameR, if True apply
            f = self.frameR.value()
            if f == False :
                n['first'].setValue(nstart)
                n['last'].setValue(nend)
                n['before'].setValue(nbefore)
                n['after'].setValue(nafter)
                
                
            n['format'].setValue(nformat)
            n['on_error'].setValue(nmissing)
            n['colorspace'].setValue(ncolorspace)
            
            # Check postageS :
            p = self.postageS.value()
            if not p:
                try:
                    n['postage_stamp'].setValue(0)
                except:
                    pass
            
            n['reload'].execute()
        
        # Write Nodes
        for n in nuke.allNodes('Write'):
            #Check frameR, if True apply
            f = self.frameR.value()
            if not f:
                n['first'].setValue(nstart)
                n['last'].setValue(nend)
            n['on_error'].setValue(nmissing)
            n['colorspace'].setValue(ncolorspace)
            n['use_limit'].setValue(True)    
            
        # Check projectP, if True apply to Root
        b = self.projectP.value()
        if not b:
            root = nuke.root()
            root['first_frame'].setValue(nstart)
            root['last_frame'].setValue(nend)
            root['format'].setValue(nformat)

                    
    def create_hierarchy(self):
        """Creates the hierarchy """
        result = nukescripts.PythonPanel.showModalDialog(self)
        if result:
            self.master_read()

            # Create Hierarchy and set postitions
            master_x = self.masterR.xpos()
            master_y = self.masterR.ypos()
            passes_list = self.passes.value().split("\n")
            offset = 150
            index=0
            first_loop=True
            passe_name = self.dirFile + ".VRay"
            nodes_list=[]
            for p in passes_list :
                if first_loop:
                    r = nuke.nodes.Read()
                    d = nuke.nodes.Dot(inputs=[r])
                    m = nuke.nodes.Merge2(Achannels='rgb', Bchannels='rgb', operation='plus', output='rgb', inputs=[self.masterR, d])
                    first_loop = False

                else:
                    r = nuke.nodes.Read()
                    d = nuke.nodes.Dot(inputs=[r])
                    m = nuke.nodes.Merge2(Achannels='rgb', Bchannels='rgb', operation='plus', output='rgb', inputs=[nuke.selectedNode(), d])

                m.setXpos(master_x)
                m.setYpos(master_y + offset)
                m.knob('selected').setValue(True)
                d['label'].setValue(p)
                d.setYpos(m.ypos())
                d.setXpos(m.xpos()+offset)
                r.setXpos(d.xpos() - 33)
                r.setYpos(d.ypos() - 100)
                r['file'].setValue(passe_name + p + ".%04d."+ self.extension)
                offset += 100
                index+=1
                nodes_list.append(r)
                nodes_list.append(d)
                nodes_list.append(m)
            
            if self.occlu.value() != "" :
			
                r = nuke.nodes.Read()
                r['file'].setValue(self.occlu.value())
                d = nuke.nodes.Dot(inputs=[r])
                m = nuke.nodes.Merge2(Achannels='rgba', Bchannels='rgba', operation='multiply',output='rgba',inputs=[nuke.selectedNode(), d])
                m.knob('selected').setValue(True)
                m.setXpos(master_x)
                m.setYpos(master_y + offset)
                d['label'].setValue("Occlusion")
                d.setYpos(m.ypos())
                d.setXpos(m.xpos() + offset)
                r.setXpos(d.xpos() - 33)
                r.setYpos(d.ypos() - 100)
                nodes_list.append(r)
                nodes_list.append(d)
                nodes_list.append(m)
				
            #End of Chain
            End = nuke.nodes.Dot(inputs=[nuke.selectedNode()])
            nodes_list.append(End)
			
            #Backdrop
            for n in nuke.allNodes():
                n.knob('selected').setValue(False)
            for n in nodes_list:
                n.setSelected(True)
            nukescripts.autoBackdrop()
            
            self.ModifyNodes()

        else:
            print "Error Creating UI"

    
def show_ui():
    return MyComp().create_hierarchy()
    
show_ui()
            
