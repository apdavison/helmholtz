===========================================
HELMHOLTZ: 
===========================================

A customizable framework for neurophysiology data management
------------------------------------------------------------
Databasing of experimental neurophysiology data together with the annotations/metadata needed to understand it promises major payoffs both for the scientists who generate the data and for the progress of neuroscience in general.

However, systematically putting the annotations and other metadata into a digital form is generally an arduous task at present, and the benefits difficult to realize, so that the cost/benefit ratio for the experimentalist is a poor one, with the corollary that the flow of data shared with the broader community is more a trickle than a flood.

To improve this situation requires tools that make it easier for neuroscientists to put their data into a database, to annotate it appropriately, to obtain some immediate benefit from the effort, and to share the data with others, under terms they control, if they so wish.

Here we present Helmholtz, an open-source framework for developing databases that are customized to the needs of individual neurophysiology labs, named after the 19th century physicist and physiologist `Hermann Ludwig Ferdinand von Helmholtz` for his work on perception.

The tension between immediate benefit in having a better tool for scientists to manage their own data and longer-term considerations of sharing with others has several implications:
    * the metadata stored should be **customizable**, since the needs of different labs can vary widely, but there should also be a common core to ensure interoperability if the data are published
    * we should support storing both **raw and processed/analyzed data**, so that the scientist can manage all phases of their workflow and so that the provenance of an individual result or graph can be easily tracked
    * the same tool should be usable both as both **local and public resource**
    * both data and metadata should have **fine-grained** and **easy-to-use** access controls


Web Solution
------------
The framework is built on top of the Django web framework (http://www.djangoproject.com/). The advantages of using a web framework are:
    * it makes it **easy to setup** either a **public or local database** (Django comes with a simple built-in web-server)
    * a **highly modular structure** makes the database **easy to customize and extend**
    * **abstraction of the underlying database layer**, so that 
        * any supported relational database can be used (e.g. MySQL, PostgreSQL, Oracle or the built-in SQLite)
        * knowledge of SQL is not required, making it **easy for non-database specialists to develop tools and extensions**
    * it is easy to develop **multiple interfaces**, e.g. a web interface, a web-services interface, interfaces to desktop acquisition or analysis software


Architecture
------------
Helmholtz provides core components which handle elements that are common to all or many domains of neurophysiology. For example, information about data acquisition: metadata for **experimental setups** (equipment, etc.), **subjects** (species, weight, anaesthesia, surgery, etc.), **stimulation** and **recording protocols**, for electrophysiology (in vivo and in vitro), optical imaging and morphological reconstructions.

A generic form of referencing supports databasing of **measurements** and **analysis** methods and steps, which can be linked to any object in the database, supplying the first building block for additional operations.

Each component of the structure is represented as a Django application and has a database table associated with it.
(figures/helmholtz_architecture.png)

Extension components to support the specific needs of individual labs are straightforward to write, requiring minimal programming experience.
(figures/base_schematic.png (Neo 0.3 architecture))

In order to explain the principles underlying Helmholtz architecture, let's take a closer look at the central data structures representing metadata associated with recordings.
 
Following interoperability directions, Helmholtz structures for recording metadata mirror those in `NEO <http://pythonhosted.org/neo/>`_, a python package for representing hierarchies of electrophysiology data and metadata, together with support for reading and writing a wide range of neurophysiology file formats, including Spike2, NeuroExplorer, AlphaOmega, Axon, Blackrock, Plexon, Tdt, Matlab and HDF5.

A direct mapping of Neo's object at attribute level exists among **Block**, **Segment** (with reference to the protocol presentation), analog and discrete **Signal**, the actual recordings.

These objects are integrated seamlessly into Helmholtz architecture, by including references to the experiment and stimulation metadata that generated the recordings, as well as the storage location of files containing the recordings.
(figures/recording.png)



==================
Helmholtz Workflow
==================

To create an experiment, some other information should be already present in helmholtz.
This is due to the fact that an experiment is not happening in the void.
In order to be able to insert a new experiment, with its results, the following steps are necessary (others are optional).

Notes
-----
* In order to use the following http addresses you need to authenticate on the server.

* The structure of each address is made of:
	* a **constant base** (`https://www.dbunic.cnrs-gif.fr/brainscales`)
	* a **resource group** (Ex: `/people`, `/device`, `/species`)
	* a **resource** (Ex: `/supplier`, `/item`, `/recordingchannel`)
	* (an optional **schema** to show resource's structure)
	* a **format** of retrieved data (Ex: `?format=xml`) 

* Many of the base resources have been already (at least partially) filled with default values.

* During the creation of a resource instance all properties of a resource have to be provided, even if null.

* Using the python interface, the http address are managed internally, and the user just use the resource name. But the structure and hierarchical requirement still holds.



1. People
---------
The researchers taking part in the experiment (with their position), the institution holding it, the suppliers of devices, are all required to create a new experiment.

Users are defined on the server (by the Admin):
	https://www.dbunic.cnrs-gif.fr/brainscales/people/user/schema?format=xml

There is a one to one mapping of a researcher onto a user. Researcher is used to add information regarding affiliation and position:
	https://www.dbunic.cnrs-gif.fr/brainscales/people/researcher/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/people/position/schema?format=xml

Similarly, an organization stores the institution hosting the researchers and devices for experiments:
	https://www.dbunic.cnrs-gif.fr/brainscales/people/organization/schema?format=xml

The same holds for the companies which supply materials for the experiment:
	https://www.dbunic.cnrs-gif.fr/brainscales/people/supplier/schema?format=xml



2. Setup
--------
The setup used in the experimental room has also to be already present. It is composed of several items grouped in subsystems.

The institution hosting the experiment is required to define a setup:
	https://www.dbunic.cnrs-gif.fr/brainscales/people/organization/?format=xml

Several items may compose a setup:
	https://www.dbunic.cnrs-gif.fr/brainscales/devices/item/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/devices/item/?format=xml

And the items may be grouped in subsystems:
	https://www.dbunic.cnrs-gif.fr/brainscales/devices/subsystem/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/devices/subsystem/?format=xml

All these resources build up a setup:
	https://www.dbunic.cnrs-gif.fr/brainscales/devices/setup/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/devices/setup/?format=xml



3. Preparation
--------------
The day of the experiment, a preparation is made ready. It represents an animal, source of the material onto which the experiment is done, together with solutions (bath, cutting).

None of the resources listed here are necessary to create an experiment, but they refer to important elements for further reference and analysis.

The definition of a preparation can have an animal:
	https://www.dbunic.cnrs-gif.fr/brainscales/preparations/animal/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/preparations/animal/?format=xml

In turn, its definition requires a strain (and a supplier, if available):
	https://www.dbunic.cnrs-gif.fr/brainscales/people/supplier/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/species/strain/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/species/strain/?format=xml

which in turn refers to a species (already defined in helmholtz):
	https://www.dbunic.cnrs-gif.fr/brainscales/species/species/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/species/species/?format=xml

In addition, it is possible to define solutions used in the preparation:
	https://www.dbunic.cnrs-gif.fr/brainscales/chemistry/solution/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/chemistry/solution/?format=xml

Finally (or directly, since the properties above are optional), a preparation can be defined:
	https://www.dbunic.cnrs-gif.fr/brainscales/preparations/preparation/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/preparations/preparation/?format=xml



4. Experiment
-------------
Having some basic resources information available in the db, it is possible to create a new experiment. A setup and at least one researcher (and optionally a preparation) are required to create an experiment:
	https://www.dbunic.cnrs-gif.fr/brainscales/people/researcher/?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/devices/setup/?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/preparations/preparation/?format=xml
With these at hand, a new experiment can finally be created:
	https://www.dbunic.cnrs-gif.fr/brainscales/experiment/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/experiment/?format=xml



5. Recordings
-------------
The outcome of an experiment is a set of recordings. The starting point to access them is a Block, representing a starting point (good cell or other). The the real recording starts
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/block/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/block/?format=xml

A stimulus is necessary (even just a non-stimulus like spontaneous activity) in order to create a new recording. There are sevaral types of possible stimulations, the complete (extensible) list is available here:
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type?format=xml

At the moment we have, as types:
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/dense_noise?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/flashing_bar?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/gabor_flash?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/gabor_noise?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/gaby?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/hexa_gabor?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/iv_curve?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/moving_bar?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/nature_noise_network?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/sparse_noise?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/spontaneous_activity?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/drifting_grating?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/type/multistim?format=xml

An actual stimulus is defined in:
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/stimulus/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/stimulus/?format=xml
For example:
	https://www.dbunic.cnrs-gif.fr/brainscales/stimulations/stimulus/5?format=xml

A storage file is necessary to create a new recording. In order to create a new file resource is required only its name (path, mimetype, size are optional):
	https://www.dbunic.cnrs-gif.fr/brainscales/storage/file/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/storage/file/?format=xml

Then we can create a new recording (modelled closely after `NEO <http://pythonhosted.org/neo/>`_):
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/recording/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/recording/?format=xml

It can be made of several segments:
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/segment/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/segment/?format=xml

Each of them can have several signals, either continuous (analog, in NEO terms):
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/continuoussignal/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/continuoussignal/?format=xml

or discrete (like Spiketrains, in NEO terms):
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/discretesignal/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/discretesignal/?format=xml

Signals can be grouped by recording channel of acquisition (with the possibility to specify a `/device/item`):
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/recordingchannel/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/recordings/recordingchannel/?format=xml


6. Analysis
-----------
The recordings are then analyzed in various steps. Often the output of one analysis step is the input to another. We can capture this analysis flow using DataSources, which are mapping recordings in terms of analysis:
	https://www.dbunic.cnrs-gif.fr/brainscales/analysis/datasource/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/analysis/datasource/?format=xml

DataSources are used and produced in analysis steps:
	https://www.dbunic.cnrs-gif.fr/brainscales/analysis/step/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/analysis/step/?format=xml

Often the final result of an analysis flow is an Image (one or more):
	https://www.dbunic.cnrs-gif.fr/brainscales/analysis/image/schema?format=xml
	https://www.dbunic.cnrs-gif.fr/brainscales/analysis/image/?format=xml
