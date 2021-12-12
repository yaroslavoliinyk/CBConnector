<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PP_dev\channel_beam\ChannelBeam.py</Name>
        <Title>Channel beam</Title>
        <Version>1.0.4.2</Version>
		<ReadLastInput>True</ReadLastInput>
    </Script>

    <Page>
        <Name>Page1</Name>
        <Text>Main page</Text>
        <Parameter>
            <Name>LeftBeamSameAsRightCheckbox</Name>
            <Text>Left girder same as right?</Text>
            <Value>True</Value>
            <ValueType>Checkbox</ValueType>
        </Parameter>
        <Parameter>
            <Name>CreateAsPythonPartCheckbox</Name>
            <Text>Create as PythonPart</Text>
            <Value>True</Value>
            <ValueType>Checkbox</ValueType>
        </Parameter>
        <Parameter>
            <Name>CreateViewsCheckbox</Name>
            <Text>Create views</Text>
            <Value>False</Value>
            <ValueType>Checkbox</ValueType>
        </Parameter>
        <Parameter>
            <Name>XHandleOffset</Name>
            <Text>Girder spacing</Text>
            <Value>3176.2</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
            <!--<Visible>False</Visible>-->
        </Parameter>
        <Parameter>
            <Name>ZHandleOffset</Name>
            <Text>Girder vertical offset</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <MaxValue>LeftBeamHeight</MaxValue>
            <MinValue>-LeftBeamHeight</MinValue>
            <!--<Visible>False</Visible>-->
        </Parameter>
        <Parameter>
            <Name>ZRotationAngle</Name>
            <Text>Rotation about the z-axis</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
        </Parameter>
        <Parameter>
            <Name>WeightAttributeCombobox</Name>
            <Text>Weight attribute measurement</Text>
            <Value>Lb</Value>
            <ValueList>Kg|Lb</ValueList>
            <ValueType>StringCombobox</ValueType>
        </Parameter>
        <Parameter>
            <Name>LeftBeamSettingsExpander</Name>
            <Text>Left beam</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>LeftBeamHeight</Name>
                <Text>Height</Text>
                <Value>1447.8</Value>
                <ValueType>Length</ValueType>
                <MinValue>300</MinValue>
            </Parameter>
            <Parameter>
                <Name>LeftBeamFlangeThickness</Name>
                <Text>Flange thickness</Text>
                <Value>25.4</Value>
                <ValueType>Length</ValueType>
                <MaxValue>LeftBeamHeight / 3</MaxValue>
                <MinValue>0</MinValue>
            </Parameter>
            <Parameter>
                <Name>LeftBeamWebThickness</Name>
                <Text>Web thickness</Text>
                <Value>25.4</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>LeftBeamZOffset</Name>
                <Text>Offset from flange</Text>
                <Value>406.4</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>LeftBeamXOffset</Name>
                <Text>Offset from web</Text>
                <Value>76.2</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>RightBeamSettingsExpander</Name>
            <Text>Right beam</Text>
            <ValueType>Expander</ValueType>
            <Visible>not LeftBeamSameAsRightCheckbox</Visible>
            <Parameter>
                <Name>RightBeamHeight</Name>
                <Text>Height</Text>
                <Value>1447.8</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>RightBeamFlangeThickness</Name>
                <Text>Flange thickness</Text>
                <Value>25.4</Value>
                <ValueType>Length</ValueType>
                <MaxValue>RightBeamHeight / 3</MaxValue>
                <MinValue>0</MinValue>
            </Parameter>
            <Parameter>
                <Name>RightBeamWebThickness</Name>
                <Text>Web thickness</Text>
                <Value>25.4</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>RightBeamZOffset</Name>
                <Text>Offset from flange</Text>
                <Value>406.4</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>RightBeamXOffset</Name>
                <Text>Offset from web</Text>
                <Value>76.2</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>Page2</Name>
        <Text>Beam</Text>

        <Parameter>
            <Name>BeamTypeRadioGroup</Name>
            <Text>Beam type</Text>
            <Value>1</Value>
            <ValueType>RadioButtonGroup</ValueType>

            <Parameter>
                <Name>ChannelBeamRadioButton</Name>
                <Text>Channel beam</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>HBeamRadioButton</Name>
                <Text>W section</Text>
                <Value>2</Value>
                <Enable>LeftConnectorPlateCheckbox and RightConnectorPlateCheckbox</Enable>
                <ValueType>RadioButton</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>BeamSettingsExpander</Name>
            <Text>Diaphragm Beam</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>IsRoundedChannelBeam</Name>
                <Text>Is rounded?</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>BeamRightBoltsSameAsLeft</Name>
                <Text>Symmetric bolts</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <!--#include ChannelBeam_Section_Settings.incpyp;ChannelBeam,0 -->
            <Parameter>
                <Name>SectionName</Name>
                <Text>Section name</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>
            <Parameter>
                <Name>CBeamSettingsName</Name>
                <Text>C-Beam Settings</Text>
                <Value>C10X15.3</Value>
                <ValueType>String</ValueType>
                <Visible>False</Visible>
            </Parameter>
            <Parameter>
                <Name>HBeamSettingsName</Name>
                <Text>C-Beam Settings</Text>
                <Value>W14X22</Value>
                <ValueType>String</ValueType>
                <Visible>False</Visible>
            </Parameter>
            <Parameter>
                <Name>CBeamSettingsUnit</Name>
                <Text>C-Beam Settings Unit</Text>
                <Value>imperial</Value>
                <ValueType>String</ValueType>
                <Visible>False</Visible>
            </Parameter>
            <Parameter>
                <Name>HBeamSettingsUnit</Name>
                <Text>C-Beam Settings Unit</Text>
                <Value>imperial</Value>
                <ValueType>String</ValueType>
                <Visible>False</Visible>
            </Parameter>
            <Parameter>
                <Name>SectionRbNumber</Name>
                <Text>Section rb number</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <Visible>False</Visible>
            </Parameter>
            <Parameter>
                <Name>SectionSelectButton</Name>
                <Text> </Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>SectionSelectButton</Name>
                    <Text>Select</Text>
                    <EventId>1000</EventId>
                    <ValueType>Button</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>BeamStartLength</Name>
                <Text>Start entry length</Text>
                <Value>50</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <!--     Invisible now, entry height = 0 -->
            <Parameter>
                <Name>BeamStartHeight</Name>
                <Text>Start entry height</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <Visible>False</Visible>
            </Parameter>
            <Parameter>
                <Name>BeamEndLength</Name>
                <Text>End entry length</Text>
                <Value>50</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <!--     Invisible now, entry height = 0 -->
            <Parameter>
                <Name>BeamEndHeight</Name>
                <Text>End entry height</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <Visible>False</Visible>

            </Parameter>
        </Parameter>

    </Page>

    <Page>
        <Name>Page3</Name>
        <Text>Stiffener plates</Text>
        <Parameter>
            <Name>LeftStiffenerPlateSettingsExpander</Name>
            <Text>Left stiffener plate settings</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>RightStiffenerSameAsLeft</Name>
                <Text>Right stiffener plate same as left?</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>LeftOuterStiffenerCheckbox</Name>
                <Text>Left outer stiffener plate</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>RightOuterStiffenerCheckbox</Name>
                <Text>Right outer stiffener plate</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
                <Visible>not RightStiffenerSameAsLeft</Visible>
            </Parameter>
            <Parameter>
                <Name>LeftStiffenerPlateWidth</Name>
                <Text>Width</Text>
                <Value>196.85</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>LeftStiffenerPlateThickness</Name>
                <Text>Thickness</Text>
                <Value>25.4</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Row1</Name>
                <Text> </Text>
                <TextId>9999</TextId>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>WidthHeader</Name>
                    <Value>Width</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>HeightHeader</Name>
                    <Value>Height</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>Row2</Name>
                <Text>Inner slope</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>LeftStiffenerPlateInnerSlopeWidth</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
                <Parameter>
                    <Name>LeftStiffenerPlateInnerSlopeHeight</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>Row3</Name>
                <Text>Top outer slope</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>LeftStiffenerPlateTopOuterSlopeWidth</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
                <Parameter>
                    <Name>LeftStiffenerPlateTopOuterSlopeHeight</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>Row4</Name>
                <Text>Bottom outer slope</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>LeftStiffenerPlateBottomOuterSlopeWidth</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
                <Parameter>
                    <Name>LeftStiffenerPlateBottomOuterSlopeHeight</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
            </Parameter>

        </Parameter>
        <Parameter>
            <Name>RightStiffenerPlateSettingsExpander</Name>
            <Text>Right stiffener plate settings</Text>
            <ValueType>Expander</ValueType>
            <Visible>not RightStiffenerSameAsLeft</Visible>

            <Parameter>
                <Name>RightStiffenerPlateWidth</Name>
                <Text>Width</Text>
                <Value>196.85</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>RightStiffenerPlateThickness</Name>
                <Text>Thickness</Text>
                <Value>25.4</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>Row5</Name>
                <Text> </Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>RightWidthHeader</Name>
                    <Value>Width</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RightHeightHeader</Name>
                    <Value>Height</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>Row6</Name>
                <Text>Inner slope</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>RightStiffenerPlateInnerSlopeWidth</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RightStiffenerPlateInnerSlopeHeight</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>Row7</Name>
                <Text>Top outer slope</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>RightStiffenerPlateTopOuterSlopeWidth</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RightStiffenerPlateTopOuterSlopeHeight</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>Row8</Name>
                <Text>Bottom outer slope</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>RightStiffenerPlateBottomOuterSlopeWidth</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RightStiffenerPlateBottomOuterSlopeHeight</Name>
                    <Value>25.4</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>Page4</Name>
        <Text>Connections</Text>
        <Parameter>
            <Name>GeneralConnectionsSettingsExpander</Name>
            <Text>General settings</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>ConnectionTypeRadioGroup</Name>
                <Text>Connection type</Text>
                <Value>2</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>ConnectionTypeRadioButtonBolt</Name>
                    <Text>Bolt option</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>ConnectionTypeRadioButtonWeld</Name>
                    <Text>Weld option</Text>
                    <Value>2</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>LeftConnectorPlateCheckbox</Name>
                <Text>Left connection plate</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
                <Enable>BeamTypeRadioGroup!=2</Enable>
            </Parameter>
            <Parameter>
                <Name>RightConnectorPlateCheckbox</Name>
                <Text>Right connection plate</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
                <Enable>BeamTypeRadioGroup!=2</Enable>
                <Visible>LeftConnectorPlateSameAsRightCheckbox == False</Visible>
            </Parameter>
            <Parameter>
                <Name>LeftConnectorPlateSameAsRightCheckbox</Name>
                <Text>Same stiffener connections</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
                <!--<Visible>LeftConnectorPlateCheckbox and RightConnectorPlateCheckbox</Visible>-->
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>ConnectorPlatesSettingsExpander</Name>
            <Text>Left connection</Text>
            <ValueType>Expander</ValueType>
            <Visible>LeftConnectorPlateCheckbox</Visible>
            #include ChannelBeam_Connector_Plate_Settings.incpyp;Left,Left
            #include ChannelBeam_Bolt_Settings.incpyp;ConnectorLeft,ConnectorLeft
        </Parameter>
        <Parameter>
            <Name>ConnectorPlatesSettingsExpander</Name>
            <Text>Right connection</Text>
            <ValueType>Expander</ValueType>
            <Visible>RightConnectorPlateCheckbox and not(LeftConnectorPlateCheckbox and LeftConnectorPlateSameAsRightCheckbox)</Visible>
            #include ChannelBeam_Connector_Plate_Settings.incpyp;Right,Right
            #include ChannelBeam_Bolt_Settings.incpyp;ConnectorRight,ConnectorRight
        </Parameter>

        <Parameter>
            <Name>LeftBeamBoltsSettingsExpander</Name>
            <Text>Stiffener plate bolts - Left end</Text>
            <ValueType>Expander</ValueType>
            <Visible>ConnectionTypeRadioGroup == 1</Visible>
            #include ChannelBeam_Bolt_Settings.incpyp;BeamLeft,BeamLeft
        </Parameter>
        <Parameter>
            <Name>RightBeamBoltsSettingsExpander</Name>
            <Text>Stiffener plate bolts - Right end</Text>
            <ValueType>Expander</ValueType>
            <Visible>not BeamRightBoltsSameAsLeft and ConnectionTypeRadioGroup == 1</Visible>
            #include ChannelBeam_Bolt_Settings.incpyp;BeamRight,BeamRight
        </Parameter>
    </Page>

    <Page>
        <Name>Page5</Name>
        <Text>Shear Studs</Text>
        <Parameter>
            <Name>StudShowCheckbox</Name>
            <Text>Create studs</Text>
            <Value>True</Value>
            <ValueType>Checkbox</ValueType>
        </Parameter>
        <Parameter>
            <Name>StudLength</Name>
            <Text>Length</Text>
            <Value>127</Value>
            <ValueType>Length</ValueType>
            <Visible>StudShowCheckbox</Visible>
        </Parameter>
        <Parameter>
            <Name>StudBodyDiameter</Name>
            <Text>Body diameter</Text>
            <Value>25.4</Value>
            <ValueType>Length</ValueType>
            <Visible>StudShowCheckbox</Visible>
        </Parameter>
        <Parameter>
            <Name>StudHeadDiameter</Name>
            <Text>Head diameter</Text>
            <Value>50.8</Value>
            <ValueType>Length</ValueType>
            <Visible>StudShowCheckbox</Visible>
        </Parameter>
        <Parameter>
            <Name>StudHeadHeight</Name>
            <Text>Head height</Text>
            <Value>25.4</Value>
            <ValueType>Length</ValueType>
            <Visible>StudShowCheckbox</Visible>
        </Parameter>
        <Parameter>
            <Name>StudNumber</Name>
            <Text>Number of studs</Text>
            <Value>10</Value>
            <ValueType>Integer</ValueType>
            <Visible>StudShowCheckbox</Visible>
        </Parameter>
        <Parameter>
            <Name>StudStartDistance</Name>
            <Text>Start distance</Text>
            <Value>127</Value>
            <ValueType>Length</ValueType>
            <MinValue>0</MinValue>
            <Visible>StudShowCheckbox</Visible>
        </Parameter>
        <Parameter>
            <Name>StudEndDistance</Name>
            <Text>End distance</Text>
            <Value>127</Value>
            <ValueType>Length</ValueType>
            <MinValue>0</MinValue>
            <Visible>StudShowCheckbox</Visible>
        </Parameter>
    </Page>

     <Page>
        <Name>Page6</Name>
        <Text>Views</Text>
        <Parameter>
            <Name>GeneralViewSettingsExpander</Name>
            <Text>General view settings</Text>
            <ValueType>Expander</ValueType>
            <Visible>CreateViewsCheckbox</Visible>
            <Parameter>
                <Name>SameWeldSymbolSettingsForAllCheckbox</Name>
                <Text>Same weld symbol settings for all</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>ShowDimensionInInchesCheckbox</Name>
                <Text>Show stiffener plate sizes in inches</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>ShowLeftBeamTextCheckbox</Name>
                <Text>Show left beam text</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>ShowRightBeamTextCheckbox</Name>
                <Text>Show right beam text</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>FrontViewTextSettingsExpander</Name>
            <Text>Dimension text settings</Text>
            <ValueType>Expander</ValueType>
            <Visible>CreateViewsCheckbox</Visible>
            <Parameter>
                <Name>LeftBeamSpecialText</Name>
                <Text>Left beam</Text>
                <Value>Fascia girder</Value>
                <ValueType>String</ValueType>
                <Visible>ShowLeftBeamTextCheckbox</Visible>
            </Parameter>
            <Parameter>
                <Name>RightBeamSpecialText</Name>
                <Text>Right beam</Text>
                <Value>Interior girder</Value>
                <ValueType>String</ValueType>
                <Visible>ShowRightBeamTextCheckbox</Visible>
            </Parameter>
            <Parameter>
                <Name>GirderSpacingTailingText</Name>
                <Text>Girder spacing</Text>
                <Value>Beam spacing</Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>LeftBeamDepthTailingText</Name>
                <Text>Left beam depth</Text>
                <Value>Beam depth</Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>RightBeamDepthTailingText</Name>
                <Text>Right beam depth</Text>
                <Value>Beam depth</Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>LeftBoltPitchTailingText</Name>
                <Text>Left bolt pitch</Text>
                <Value>Bolt pitch</Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>LeftBoltEdgeDistanceTailingText</Name>
                <Text>Left bolt edge distance</Text>
                <Value>Min. edge distance</Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>RightBoltPitchTailingText</Name>
                <Text>Right bolt pitch</Text>
                <Value>Bolt pitch</Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>RightBoltEdgeDistanceTailingText</Name>
                <Text>Right bolt edge distance</Text>
                <Value>Min. edge distance</Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>LeftStiffenerPlateTailingText</Name>
                <Text>Left stiffener plate</Text>
                <Value>Bearing stiffener</Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>RightStiffenerPlateTailingText</Name>
                <Text>Right stiffener plate</Text>
                <Value>Bearing stiffener</Value>
                <ValueType>String</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>WeldingSymbolSettingsAllExpander</Name>
            <Text>Welding symbol settings - All</Text>
            <ValueType>Expander</ValueType>
            <Visible>CreateViewsCheckbox and SameWeldSymbolSettingsForAllCheckbox</Visible>

            #include ChannelBeam_Weld_Symbol_Settings.incpyp;All,All

        </Parameter>
        <Parameter>
            <Name>WeldingSymbolSettingsLeftAngledBeamChannelBeamExpander</Name>
            <Text>Welding symbol settings - left girder, channel beam</Text>
            <ValueType>Expander</ValueType>
            <Visible>CreateViewsCheckbox and not SameWeldSymbolSettingsForAllCheckbox</Visible>

            #include ChannelBeam_Weld_Symbol_Settings.incpyp;ChannelBeamStart,ChannelBeamStart

        </Parameter>
        <Parameter>
            <Name>WeldingSymbolSettingsRightAngledBeamChannelBeamExpander</Name>
            <Text>Welding symbol settings - right girder, channel beam</Text>
            <ValueType>Expander</ValueType>
            <Visible>CreateViewsCheckbox and not SameWeldSymbolSettingsForAllCheckbox</Visible>

            #include ChannelBeam_Weld_Symbol_Settings.incpyp;ChannelBeamEnd,ChannelBeamEnd

        </Parameter>
    </Page>


</Element>