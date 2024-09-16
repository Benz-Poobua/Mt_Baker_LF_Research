# DLP_Mt_Baker: Distinguishing Long-Period Seismic Sources at Mt. Baker Volcano
This repository hosts code and metadata for analyzing long-period seismic events at Mt. Baker volcano in Washington state, USA.

## Repository Structure  
 - data - unprocessed or minimally processed data files  
    - Events - Data files for seismic catalog metadata  
    - Sensors - Data files for geophysical instrument metadata  
 - docs - supporting files for repository documentation  
 - GIS - Geographic Information Systems files  
    - Mt_Baker_LP_Maps.qgz - QGIS project file  
 - results - output files from codes in this repository  
    - figures - Rendered figure files  
 - src - source code  
    - notebooks - Jupyter Notebook files  
    - PostgreSQL - SQL database query scripts  
    - python - python scripts  
 - environment.yml - conda environment definition (TESTING IN PROGRESS)  
 - LICENSE - distribution terms  
 - README.md - you are here!  
 - TODO.md - General ToDo list for this repository (formatted for "Todo Tree" VSCode plugin)  



## Motivation  
Mt. Baker has been seismically monitored since 1972, but produced relatively few observable volcano-tectonic earthquakes, even during its period of unrest in 1975 (Crider et al., 2011). However, Mt. Baker produces a notable amount of Deep Long Period earthquakes (DLP), which are defined as seismic events with source solutions deeper than 10 km b.s.l. and dominant periods in the 0.2 - 1 second band (1-5 Hz; see Figure 1; Nichols et al., 2011). Mt. Baker's DLP catalog accounts half of such events observed between 1980 and 2009 for all Cascades volcanoes and are attributed to magma and/or volatile migration at depth (Nichols et al., 2011; and references therein). 

![image](./docs/Nichols_etal_2011_Figure_1.jpeg)  
*Figure 1: Figure 1 in [Nichols et al. (2011)](https://doi.org/10.1016/j.jvolgeores.2010.12.005): "Seismograms and spectrograms from two events recorded on station FMW near Mt. Rainier illustrate the difference in frequency content between a VT (top—1995/07/14 12:14) and a DLP (bottom—1996/03/05 14:09). The VT contains frequencies between 1 and 20 Hz, and the DLP contains energy mostly below 5 Hz. VT and DLP hypocentral distances are 23.2 km and 23.8 km, respectively. VT and DLP maximum amplitude counts are 1554 and 253, respectively. Spectrogram colors represent amplitude intensity and range from blue (low) to yellow (intermediate) to red (high)."*

Subsequent monitoring by the PNSN added 21 more DLPs to the Mt. Baker catalog, resulting in an uptick in catalogged DLP frequency (Figure 2). This percieved rise in DLP activity is thought to be an observational artifact, arising from a combination of improvements to instrumentation, increased station density around Mt. Baker, and revised observatory practice at the PNSN motivated by findings from temporary, on-volcano seismic deployments in 1975-76 (Malone, 1977; Weaver & Malone, 1979) and 2009 (Caplan-Auerbach et al., 2009), and observation of DLPs at other Cascades volcanoes (e.g., Nichols et al., 2011).

![image](./results/figures/motivations_fig_1_120dpi.png)  
*Figure 2: Origin times and depths (left axis) of PNSN catalog 'lf' events within 20 km of Mt. Baker that satisfy the DLP depth-based definition. Catalog events presented in Nichols et al. (2011) are shown in blue and subsequent events are shown in orange. Active station counts within 30 km of the Mt. Baker summit (red line) and annual DLP event counts (black bars) are shown for comparison (shared scaling on right axis). Station counts based on IRIS Data Management Center metadata.*

The glaciers cladding Mt. Baker (and other Cascades volcanoes) also produce long-period seismic events in the same band band as DLPs (Figure 3; from Thelen et al., 2013), and are primarily distinguised by source constraints near land-surface (Weaver and Malone, 1979; Caplain-Auerbach et al., 2009; Thelen et al., 2013; Allstadt & Malone, 2014). The relatively sparse seismic network around Mt. Baker results in only the largest LP events are sufficient to generate an subnet trigger in the PNSN's automated detection pipeline, meaning that lower magnitude DLPs may be difficult to distinguish from glacier-sourced LPs or missed entirely (as discussed in Thelen et al., 2013). Moreover, surface events have only recently been retained in the PNSN catalog as standard practice, meaning that smaller DLPs may have been missed due to prior analyst policies.

![image](./docs/Thelen_etal_2013_Figure%202.gif)
*Figure 3: Figure 2 in [Thelen et al. (2013)](https://doi.org/10.3189/2013Jog12J111): "Example of various types of waveforms (a) and their spectra (b) recorded on Mount Rainier at short-period vertical station RCS. The amplitude scale is normalized for each waveform, with the maximum amplitudes for each waveform given in counts on the left. Gray triangles indicate time windows for spectra. In order from the top of the plot: glacial earthquake, multiplet 5 of this sequence; inferred icequake; M1.2 tectonic earthquake located ∼20 km east of Mount Rainier; M0.6 volcano-tectonic earthquake located 2.5 km below the mountain from a September 2009 swarm; M2.3 deep long-period earthquake 13.6 km below Mount Rainier; avalanche on 5 June 2010; inferred rockfall near Willis Wall 7 June 2010."*

Advances in seismic analysis tools and computing power give us the ability to quickly re-analyze large volumes of wavefrom data, overcoming a substantial hurdle to earlier researchers (e.g., Mousavi & Beroza, 2023). These include efficient template matching workflows (e.g,. Hotovec-Ellis and Jefferies, 2016; Chamberlain et al., 2017), machine-learning models specifically trained to detect and classify DLP earthquakes (Münchmeyer et al., 2024) and deep learning models trained to descriminate between various source types (Kharita et al., 2024). All of which can be deployed on data from individual seismometers. In this study we will conduct a review of LP events localized to Mt. Baker in the PNSN catalog and used reviewed event classifications to inform a systematic search across the entirety of digitally available waveform data for stations proximal to Mt. Baker to enhance the current catalog. Through this analysis we hope to address the following questions:

## Research Questions  
1) Does the PNSN catalog represent a comprehensive set of DLPs for Mt. Baker?  
2) Is the percieved uptick in cataloged DLPs in the past decade an observational artifact, as hypothesized?  
3) Can we identify dependable time-series-derived characteristics to differentiate DLP and glacier-sourced LP events at Mt. Baker?  
4) How similar are DLPs and what can this tell us about their source processes?

## Research Stages
1) Catalog Survey: review the [PNSN](https://pnsn.org/events?custom_search=true) and [REDpy](https://assets.pnsn.org/red/) catalogs to:
    - verify accurate classifications of 'LF' (for DLPs) and 'SU' (for shallow LPs)  
    - assess if DLPs and glacier LPs are triggering clusters in the repeating earthquake catalog.  

2) Catalog Classification Refinement: refine classifications of long period events using features identified in the literature and new features that arise from observations in step 1. Refined classes might be:  
    - deep long-period (DLP)  
    - shallow long-period (SLP) or glacier long-period (GLP)
    - under-constrained long-period (LP)   

3) Catalog Enhancement: enhance the PNSN long-period seismicity catalog at Mt. Baker using observations from steps 1-2 and one or more of the following analytic approaches:   
    - Waveform cross correlation / template matching using [EQcorrscan](https://eqcorrscan.readthedocs.io/en/latest/) (after Thelen et al., 2013). 
    - Detection/phase picking with the low-frequency earthquake detection model [LFEDetect](https://seisbench.readthedocs.io/en/stable/pages/documentation/models.html#seisbench.models.lfe_detect.LFEDetect) distributed with [SeisBench](https://seisbench.readthedocs.io).
    - Feature-driven detection/classification (e.g., Kharita et al., 2024). 

4) Interpretation: review the enhanced catalog to determine if meaningful patterns exist that better inform our understanding of magmatic processes at Mt. Baker.

## License  
![image](./docs/gplv3-with-text-136x68.png)  
Original works contained in this repository are distributed under the attached GNU General Public License v3. Figures from cited works must follow the individual licenses of the cited works (i.e., Figures 1 and 3 in the Motivation section).  


## Originating Author  
Nathan T. Stevens (PNSN Seismologist/Developer) - Research Mentor  

## Project Collaborators
Benz Poobua (ESS Undergraduate Researcher) - Research Mentee  
Renate Hartog (PNSN Network Manager) - Research Supervisor  
Steve Malone (PNSN Director Emeritus)  
Alex Hutko (PNSN Research Seismologist)  

## Collaborating Organizations  
 - [PNSN Scientific Products Team](https://pnsn.org)  
 - [UW ESS Department Researchers](https://ess.uw.edu)    
 - [USGS Cascade Volcano Observatory Researchers](https://www.usgs.gov/observatories/cvo)  

## Collaborator Documents Repository  
A repository of written documents and references for permissioned collaborators is available on the PNSN GoogleDrive.  

## Works Cited
 - [Allstadt, K., and Malone, S.D. (2014) Swarms of repeating stick-slip ice-quakes triggered by snow loading at Mt. Rainier volcano. JGR-Earth Surface, 119, 1180-1203](https://doi.org/10.1002/2014JF003086).

 - [Caplan-Auerbach, J., Thelen, W.A., and Moran, S.C. (2009) An Unusual Cluster of Low-Frequency Earthquakes at Mount Baker, Washington, as Detected by a Local Broadband Network. EOS Trans. AGU 89, Fall Meeting Suppl., Paper number V23D-2111](https://ui.adsabs.harvard.edu/abs/2009AGUFM.V23D2111C/abstract)

 - [Chamberlain, C.J., Hopp, C.J., Boese, C.M., Warren-Smith, E., Chambers, D., Chu, S.X., Michailos, K., and Townsend, J. (2017) EQcorrscan: Repeating and Near-Repeating Earthquake Detection and Analysis in Python. SRL 89(1): 173-181](https://doi.org/10.1785/0220170151)

 - [Crider, J.G., Johnsen, K.H., and Williams-Jones, G. (2008) Thirty-year gravity change at Mount Baker volcano, Washington, USA: extracting the signal from under the ice. Geophys Res Lett 35:L20304– L20308](https://doi.org/10.1029/2008GL034921)

 - [Hotovec-Ellis, A.J., and Jeffries, C. (2016) Near Real-time Detection, Clustering, and Analysis of Repeating Earthquakes: Application to Mount St. Helens and Redoubt Volcanoes – Invited, presented at Seismological Society of America Annual Meeting, Reno, Nevada, 20 Apr.](https://code.usgs.gov/vsc/REDPy)

 - [Kharita, A., Denolle, M.A., West, M.E. (2024) Discrimination between icequakes and earthquakes in southern Alaska: an exploration of waveform features using Random Forest algorithm. GJI 237(2), 1189-11207](https://doi.org/10.1093/gji/ggae106)

 - [Malone, S.D. (1977) Summary of Seismicity and Gravity, pg. 19-25 in Frank, D., Meier, M.F., and Swanson, D., Assessmentof Increased THermal Activity at Mount Baker, Washington March 1975-March 1976. U.S. Geological Survey Professional Paper 1022-A](https://pubs.usgs.gov/pp/1022a/report.pdf)

 - [Mousavi, S.M., and Beroza, G.C. (2023) Machine Learning in Earthquake Seismology. Ann. Rev. Earth and Planet. Sci. 51: 105-129](https://doi.org/10.1145/annurev-earth-071822-100323)

 - [Münchmeyer, J., Giffard-Roisin, S., Malfante, M., Frank, W.B., Poli, P., Marsan, D., and Socquet, A. (2024) Deep learning detects uncataloged low-frequency earthquakes across regions. Seismica , 3(1)](https://doi.org/10.26443/seismica.v3i1.1185)

 - [Nichols, M.L., Malone, S.D., Moran, S.C., Thelen, W.A., and Vidale, J.E. (2011) Deep long-period earthquakes beneath Washington and Oregon volcanoes. J. Volc. and Geotherm. Res. 200(3–4), 116–128.](https://doi.org/10.1016/j.jvolgeores.2010.12.005)

 - [Thelen, W.A., Allstadt, K., De Angelis, S., Malone, S.D., Moran, S.C., and Vidale, J. (2013) Shallow repeating seismic events under an alpine glacier at Mount Rainier, Washington, USA. J. Glac., 59(214), 345-356.](https://doi.org/10.3189/2013Jog12J111)

 - [Weaver, C.S., and Malone, S.D. (1979) Seismic evidence for discrete glacier motion at the rock-ice interface. J. Glaciol 23:171–184](https://doi.org/10.3189/S0022143000029816)
