
- [CycloneDX](#cyclonedx)
- [Vulnerability Exploitability Exchange (VEX)](#vulnerability-exploitability-exchange-vex)
  - [Independent BOM and VEX BOM](#independent-bom-and-vex-bom)
  - [BOM With Embedded VEX](#bom-with-embedded-vex)
  - [CycloneDX and Third-Party Advisory Formats](#cyclonedx-and-third-party-advisory-formats)
  - [High-Level Object Model](#high-level-object-model)
  - [VeX reports schema](#vex-reports-schema)

---

# CycloneDX

---

# Vulnerability Exploitability Exchange (VEX)

> VEX is useful to express that while some vulnerability might be present in a software artifact via a dependency, it is actually not exploitable.

Known vulnerabilities inherited from the use of third-party and open source software and the exploitability of the vulnerabilities
can be communicated with CycloneDX. Previously unknown vulnerabilities affecting both components and services may also be disclosed
using CycloneDX, making it ideal for both VEX and security advisory use cases.
- VEX information can be represented inside an existing BOM, or in a dedicated VEX BOM
- Supports known and unknown vulnerabilities against components and services
- Communicates the vulnerability details, exploitability, and detailed analysis

## Independent BOM and VEX BOM
Inventory described in a BOM (SBOM, SaaSBOM, etc) will typically remain static until such time the inventory changes.
However, vulnerability information is much more dynamic and subject to change. Therefore, it is recommended to decouple
the VEX from the BOM. This allows VEX information to be updated without having to create and track additional BOMs.

VEX is an integral part of the CycloneDX specification providing the convenience of leveraging a single format and tool chain.

<img alt="pic" src="pic" src="pic" src="pic" src="pic" src="https://cyclonedx.org/theme/assets/images/vexbom.svg" width="500" alt="Independent BOM and VEX Document">

With CycloneDX, it is possible to reference a component, service, or vulnerability inside a BOM from other systems or
other BOMs. This deep-linking capability is referred to as BOM-Link.

**Syntax**:
```
urn:cdx:serialNumber/version#bom-ref
```

**Examples**:
```
urn:cdx:f08a6ccd-4dce-4759-bd84-c626675d60a7/1
urn:cdx:f08a6ccd-4dce-4759-bd84-c626675d60a7/1#componentA
```

| Field        | Description |
| ------------ | ----------- |
| serialNumber | The unique serial number of the BOM. The serial number MUST conform to RFC-4122. |
| version      | The version of the BOM. The default version is `1`. |
| bom-ref      | The unique identifier of the component, service, or vulnerability within the BOM. |

## BOM With Embedded VEX

<img alt="pic" src="pic" src="pic" src="pic" src="pic" src="https://cyclonedx.org/theme/assets/images/embedded-vex.svg" width="167" alt="BOM With Embedded VEX">

CycloneDX also supports embedding VEX information inside a BOM, thus having a single artifact that describes both
inventory and VEX data. There are several uses for embedding VEX data including:

* Audit use cases where inventory and vulnerability data need to be captured at a specific point in time
* Automated security tools may opt to create a single BOM with embedded vulnerability or VEX data for convenience and portability

## CycloneDX and Third-Party Advisory Formats

Every component or service defined in a CycloneDX BOM may optionally define external references to security advisory
feeds. CycloneDX is agnostic to the advisory format, however, the
[Common Security Advisory Framework (CSAF)](https://www.oasis-open.org/committees/csaf), an OASIS Open standard, is
recommended. Refer to the [Security Advisories Use Case](https://cyclonedx.org/use-cases/#security-advisories) for more information.

CSAF also supports an optional VEX profile which can be used with CycloneDX.

## High-Level Object Model
![CycloneDX Object Model Swimlane](https://cyclonedx.org/theme/assets/images/CycloneDX-Object-Model-Swimlane.svg)

---

## VeX reports schema

[bom-1.5.schema.json](https://github.com/CycloneDX/specification/blob/1.5/schema/bom-1.5.schema.json)


```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://cyclonedx.org/schema/bom-1.5.schema.json",
  "type": "object",
  "title": "CycloneDX Software Bill of Materials Standard",
  "$comment" : "CycloneDX JSON schema is published under the terms of the Apache License 2.0.",
  "required": [
    "bomFormat",
    "specVersion",
    "version"
  ],
  "additionalProperties": false,
  "properties": {
    "$schema": {
      "type": "string",
      "enum": [
        "http://cyclonedx.org/schema/bom-1.5.schema.json"
      ]
    },
    "bomFormat": {
      "type": "string",
      "title": "BOM Format",
      "description": "Specifies the format of the BOM. This helps to identify the file as CycloneDX since BOMs do not have a filename convention nor does JSON schema support namespaces. This value MUST be \"CycloneDX\".",
      "enum": [
        "CycloneDX"
      ]
    },
    "specVersion": {
      "type": "string",
      "title": "CycloneDX Specification Version",
      "description": "The version of the CycloneDX specification a BOM conforms to (starting at version 1.2).",
      "examples": ["1.5"]
    },
    "serialNumber": {
      "type": "string",
      "title": "BOM Serial Number",
      "description": "Every BOM generated SHOULD have a unique serial number, even if the contents of the BOM have not changed over time. If specified, the serial number MUST conform to RFC-4122. Use of serial numbers are RECOMMENDED.",
      "examples": ["urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79"],
      "pattern": "^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    },
    "version": {
      "type": "integer",
      "title": "BOM Version",
      "description": "Whenever an existing BOM is modified, either manually or through automated processes, the version of the BOM SHOULD be incremented by 1. When a system is presented with multiple BOMs with identical serial numbers, the system SHOULD use the most recent version of the BOM. The default version is '1'.",
      "minimum": 1,
      "default": 1,
      "examples": [1]
    },
    "metadata": {
      "$ref": "#/definitions/metadata",
      "title": "BOM Metadata",
      "description": "Provides additional information about a BOM."
    },
    "components": {
      "type": "array",
      "items": {"$ref": "#/definitions/component"},
      "uniqueItems": true,
      "title": "Components",
      "description": "A list of software and hardware components."
    },
    "services": {
      "type": "array",
      "items": {"$ref": "#/definitions/service"},
      "uniqueItems": true,
      "title": "Services",
      "description": "A list of services. This may include microservices, function-as-a-service, and other types of network or intra-process services."
    },
    "externalReferences": {
      "type": "array",
      "items": {"$ref": "#/definitions/externalReference"},
      "title": "External References",
      "description": "External references provide a way to document systems, sites, and information that may be relevant, but are not included with the BOM. They may also establish specific relationships within or external to the BOM."
    },
    "dependencies": {
      "type": "array",
      "items": {"$ref": "#/definitions/dependency"},
      "uniqueItems": true,
      "title": "Dependencies",
      "description": "Provides the ability to document dependency relationships."
    },
    "compositions": {
      "type": "array",
      "items": {"$ref": "#/definitions/compositions"},
      "uniqueItems": true,
      "title": "Compositions",
      "description": "Compositions describe constituent parts (including components, services, and dependency relationships) and their completeness. The completeness of vulnerabilities expressed in a BOM may also be described."
    },
    "vulnerabilities": {
      "type": "array",
      "items": {"$ref": "#/definitions/vulnerability"},
      "uniqueItems": true,
      "title": "Vulnerabilities",
      "description": "Vulnerabilities identified in components or services."
    },
    "annotations": {
      "type": "array",
      "items": {"$ref": "#/definitions/annotations"},
      "uniqueItems": true,
      "title": "Annotations",
      "description": "Comments made by people, organizations, or tools about any object with a bom-ref, such as components, services, vulnerabilities, or the BOM itself. Unlike inventory information, annotations may contain opinion or commentary from various stakeholders. Annotations may be inline (with inventory) or externalized via BOM-Link, and may optionally be signed."
    },
    "formulation": {
      "type": "array",
      "items": {"$ref": "#/definitions/formula"},
      "uniqueItems": true,
      "title": "Formulation",
      "description": "Describes how a component or service was manufactured or deployed. This is achieved through the use of formulas, workflows, tasks, and steps, which declare the precise steps to reproduce along with the observed formulas describing the steps which transpired in the manufacturing process."
    },
    "properties": {
      "type": "array",
      "title": "Properties",
      "description": "Provides the ability to document properties in a name-value store. This provides flexibility to include data not officially supported in the standard without having to use additional namespaces or create extensions. Unlike key-value stores, properties support duplicate names, each potentially having different values. Property names of interest to the general public are encouraged to be registered in the [CycloneDX Property Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy). Formal registration is OPTIONAL.",
      "items": {
        "$ref": "#/definitions/property"
      }
    },
    "signature": {
      "$ref": "#/definitions/signature",
      "title": "Signature",
      "description": "Enveloped signature in [JSON Signature Format (JSF)](https://cyberphone.github.io/doc/security/jsf.html)."
    }
  },
  "definitions": {
    "refType": {
      "description": "Identifier for referable and therefore interlink-able elements.",
      "type": "string",
      "minLength": 1,
      "$comment": "value SHOULD not start with the BOM-Link intro 'urn:cdx:'"
    },
    "refLinkType": {
      "description": "Descriptor for an element identified by the attribute 'bom-ref' in the same BOM document.\nIn contrast to `bomLinkElementType`.",
      "allOf": [{"$ref": "#/definitions/refType"}]
    },
    "bomLinkDocumentType": {
      "title": "BOM-Link Document",
      "description": "Descriptor for another BOM document. See https://cyclonedx.org/capabilities/bomlink/",
      "type": "string",
      "format": "iri-reference",
      "pattern": "^urn:cdx:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/[1-9][0-9]*$",
      "$comment": "part of the pattern is based on `bom.serialNumber`'s pattern"
    },
    "bomLinkElementType": {
      "title": "BOM-Link Element",
      "description": "Descriptor for an element in a BOM document. See https://cyclonedx.org/capabilities/bomlink/",
      "type": "string",
      "format": "iri-reference",
      "pattern": "^urn:cdx:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/[1-9][0-9]*#.+$",
      "$comment": "part of the pattern is based on `bom.serialNumber`'s pattern"
    },
    "bomLink": {
      "anyOf": [
        {
          "title": "BOM-Link Document",
          "$ref": "#/definitions/bomLinkDocumentType"
        },
        {
          "title": "BOM-Link Element",
          "$ref": "#/definitions/bomLinkElementType"
        }
      ]
    },
    "metadata": {
      "type": "object",
      "title": "BOM Metadata Object",
      "additionalProperties": false,
      "properties": {
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "title": "Timestamp",
          "description": "The date and time (timestamp) when the BOM was created."
        },
        "lifecycles": {
          "type": "array",
          "title": "Lifecycles",
          "description": "",
          "items": {
            "type": "object",
            "title": "Lifecycle",
            "description": "The product lifecycle(s) that this BOM represents.",
            "oneOf": [
              {
                "required": ["phase"],
                "additionalProperties": false,
                "properties": {
                  "phase": {
                    "type": "string",
                    "title": "Phase",
                    "description": "A pre-defined phase in the product lifecycle.\n\n* __design__ = BOM produced early in the development lifecycle containing inventory of components and services that are proposed or planned to be used. The inventory may need to be procured, retrieved, or resourced prior to use.\n* __pre-build__ = BOM consisting of information obtained prior to a build process and may contain source files and development artifacts and manifests. The inventory may need to be resolved and retrieved prior to use.\n* __build__ = BOM consisting of information obtained during a build process where component inventory is available for use. The precise versions of resolved components are usually available at this time as well as the provenance of where the components were retrieved from.\n* __post-build__ = BOM consisting of information obtained after a build process has completed and the resulting components(s) are available for further analysis. Built components may exist as the result of a CI/CD process, may have been installed or deployed to a system or device, and may need to be retrieved or extracted from the system or device.\n* __operations__ = BOM produced that represents inventory that is running and operational. This may include staging or production environments and will generally encompass multiple SBOMs describing the applications and operating system, along with HBOMs describing the hardware that makes up the system. Operations Bill of Materials (OBOM) can provide full-stack inventory of runtime environments, configurations, and additional dependencies.\n* __discovery__ = BOM consisting of information observed through network discovery providing point-in-time enumeration of embedded, on-premise, and cloud-native services such as server applications, connected devices, microservices, and serverless functions.\n* __decommission__ = BOM containing inventory that will be, or has been retired from operations.",
                    "enum": [
                      "design",
                      "pre-build",
                      "build",
                      "post-build",
                      "operations",
                      "discovery",
                      "decommission"
                    ]
                  }
                }
              },
              {
                "required": ["name"],
                "additionalProperties": false,
                "properties": {
                  "name": {
                    "type": "string",
                    "title": "Name",
                    "description": "The name of the lifecycle phase"
                  },
                  "description": {
                    "type": "string",
                    "title": "Description",
                    "description": "The description of the lifecycle phase"
                  }
                }
              }
            ]
          }
      },
        "tools": {
          "oneOf": [
            {
              "type": "object",
              "title": "Creation Tools",
              "description": "The tool(s) used in the creation of the BOM.",
              "additionalProperties": false,
              "properties": {
                "components": {
                  "type": "array",
                  "items": {"$ref": "#/definitions/component"},
                  "uniqueItems": true,
                  "title": "Components",
                  "description": "A list of software and hardware components used as tools"
                },
                "services": {
                  "type": "array",
                  "items": {"$ref": "#/definitions/service"},
                  "uniqueItems": true,
                  "title": "Services",
                  "description": "A list of services used as tools. This may include microservices, function-as-a-service, and other types of network or intra-process services."
                }
              }
            },
            {
              "type": "array",
              "title": "Creation Tools (legacy)",
              "description": "[Deprecated] The tool(s) used in the creation of the BOM.",
              "items": {"$ref": "#/definitions/tool"}
            }
          ]
        },
        "authors" :{
          "type": "array",
          "title": "Authors",
          "description": "The person(s) who created the BOM. Authors are common in BOMs created through manual processes. BOMs created through automated means may not have authors.",
          "items": {"$ref": "#/definitions/organizationalContact"}
        },
        "component": {
          "title": "Component",
          "description": "The component that the BOM describes.",
          "$ref": "#/definitions/component"
        },
        "manufacture": {
          "title": "Manufacture",
          "description": "The organization that manufactured the component that the BOM describes.",
          "$ref": "#/definitions/organizationalEntity"
        },
        "supplier": {
          "title": "Supplier",
          "description": " The organization that supplied the component that the BOM describes. The supplier may often be the manufacturer, but may also be a distributor or repackager.",
          "$ref": "#/definitions/organizationalEntity"
        },
        "licenses": {
          "title": "BOM License(s)",
          "$ref": "#/definitions/licenseChoice"
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "description": "Provides the ability to document properties in a name-value store. This provides flexibility to include data not officially supported in the standard without having to use additional namespaces or create extensions. Unlike key-value stores, properties support duplicate names, each potentially having different values. Property names of interest to the general public are encouraged to be registered in the [CycloneDX Property Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy). Formal registration is OPTIONAL.",
          "items": {"$ref": "#/definitions/property"}
        }
      }
    },
    "tool": {
      "type": "object",
      "title": "Tool",
      "description": "[Deprecated] - DO NOT USE. This will be removed in a future version. This will be removed in a future version. Use component or service instead. Information about the automated or manual tool used",
      "additionalProperties": false,
      "properties": {
        "vendor": {
          "type": "string",
          "title": "Tool Vendor",
          "description": "The name of the vendor who created the tool"
        },
        "name": {
          "type": "string",
          "title": "Tool Name",
          "description": "The name of the tool"
        },
        "version": {
          "type": "string",
          "title": "Tool Version",
          "description": "The version of the tool"
        },
        "hashes": {
          "type": "array",
          "items": {"$ref": "#/definitions/hash"},
          "title": "Hashes",
          "description": "The hashes of the tool (if applicable)."
        },
        "externalReferences": {
          "type": "array",
          "items": {"$ref": "#/definitions/externalReference"},
          "title": "External References",
          "description": "External references provide a way to document systems, sites, and information that may be relevant, but are not included with the BOM. They may also establish specific relationships within or external to the BOM."
        }
      }
    },
    "organizationalEntity": {
      "type": "object",
      "title": "Organizational Entity Object",
      "description": "",
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "$ref": "#/definitions/refType",
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the object elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
        },
        "name": {
          "type": "string",
          "title": "Name",
          "description": "The name of the organization",
          "examples": [
            "Example Inc."
          ]
        },
        "url": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "iri-reference"
          },
          "title": "URL",
          "description": "The URL of the organization. Multiple URLs are allowed.",
          "examples": ["https://example.com"]
        },
        "contact": {
          "type": "array",
          "title": "Contact",
          "description": "A contact at the organization. Multiple contacts are allowed.",
          "items": {"$ref": "#/definitions/organizationalContact"}
        }
      }
    },
    "organizationalContact": {
      "type": "object",
      "title": "Organizational Contact Object",
      "description": "",
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "$ref": "#/definitions/refType",
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the object elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
        },
        "name": {
          "type": "string",
          "title": "Name",
          "description": "The name of a contact",
          "examples": ["Contact name"]
        },
        "email": {
          "type": "string",
          "format": "idn-email",
          "title": "Email Address",
          "description": "The email address of the contact.",
          "examples": ["firstname.lastname@example.com"]
        },
        "phone": {
          "type": "string",
          "title": "Phone",
          "description": "The phone number of the contact.",
          "examples": ["800-555-1212"]
        }
      }
    },
    "component": {
      "type": "object",
      "title": "Component Object",
      "required": [
        "type",
        "name"
      ],
      "additionalProperties": false,
      "properties": {
        "type": {
          "type": "string",
          "enum": [
            "application",
            "framework",
            "library",
            "container",
            "platform",
            "operating-system",
            "device",
            "device-driver",
            "firmware",
            "file",
            "machine-learning-model",
            "data"
          ],
          "title": "Component Type",
          "description": "Specifies the type of component. For software components, classify as application if no more specific appropriate classification is available or cannot be determined for the component. Types include:\n\n* __application__ = A software application. Refer to [https://en.wikipedia.org/wiki/Application_software](https://en.wikipedia.org/wiki/Application_software) for information about applications.\n* __framework__ = A software framework. Refer to [https://en.wikipedia.org/wiki/Software_framework](https://en.wikipedia.org/wiki/Software_framework) for information on how frameworks vary slightly from libraries.\n* __library__ = A software library. Refer to [https://en.wikipedia.org/wiki/Library_(computing)](https://en.wikipedia.org/wiki/Library_(computing))\n for information about libraries. All third-party and open source reusable components will likely be a library. If the library also has key features of a framework, then it should be classified as a framework. If not, or is unknown, then specifying library is RECOMMENDED.\n* __container__ = A packaging and/or runtime format, not specific to any particular technology, which isolates software inside the container from software outside of a container through virtualization technology. Refer to [https://en.wikipedia.org/wiki/OS-level_virtualization](https://en.wikipedia.org/wiki/OS-level_virtualization)\n* __platform__ = A runtime environment which interprets or executes software. This may include runtimes such as those that execute bytecode or low-code/no-code application platforms.\n* __operating-system__ = A software operating system without regard to deployment model (i.e. installed on physical hardware, virtual machine, image, etc) Refer to [https://en.wikipedia.org/wiki/Operating_system](https://en.wikipedia.org/wiki/Operating_system)\n* __device__ = A hardware device such as a processor, or chip-set. A hardware device containing firmware SHOULD include a component for the physical hardware itself, and another component of type 'firmware' or 'operating-system' (whichever is relevant), describing information about the software running on the device.\n  See also the list of [known device properties](https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/device.md).\n* __device-driver__ = A special type of software that operates or controls a particular type of device. Refer to [https://en.wikipedia.org/wiki/Device_driver](https://en.wikipedia.org/wiki/Device_driver)\n* __firmware__ = A special type of software that provides low-level control over a devices hardware. Refer to [https://en.wikipedia.org/wiki/Firmware](https://en.wikipedia.org/wiki/Firmware)\n* __file__ = A computer file. Refer to [https://en.wikipedia.org/wiki/Computer_file](https://en.wikipedia.org/wiki/Computer_file) for information about files.\n* __machine-learning-model__ = A model based on training data that can make predictions or decisions without being explicitly programmed to do so.\n* __data__ = A collection of discrete values that convey information.",
          "examples": ["library"]
        },
        "mime-type": {
          "type": "string",
          "title": "Mime-Type",
          "description": "The optional mime-type of the component. When used on file components, the mime-type can provide additional context about the kind of file being represented such as an image, font, or executable. Some library or framework components may also have an associated mime-type.",
          "examples": ["image/jpeg"],
          "pattern": "^[-+a-z0-9.]+/[-+a-z0-9.]+$"
        },
        "bom-ref": {
          "$ref": "#/definitions/refType",
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the component elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
        },
        "supplier": {
          "title": "Component Supplier",
          "description": " The organization that supplied the component. The supplier may often be the manufacturer, but may also be a distributor or repackager.",
          "$ref": "#/definitions/organizationalEntity"
        },
        "author": {
          "type": "string",
          "title": "Component Author",
          "description": "The person(s) or organization(s) that authored the component",
          "examples": ["Acme Inc"]
        },
        "publisher": {
          "type": "string",
          "title": "Component Publisher",
          "description": "The person(s) or organization(s) that published the component",
          "examples": ["Acme Inc"]
        },
        "group": {
          "type": "string",
          "title": "Component Group",
          "description": "The grouping name or identifier. This will often be a shortened, single name of the company or project that produced the component, or the source package or domain name. Whitespace and special characters should be avoided. Examples include: apache, org.apache.commons, and apache.org.",
          "examples": ["com.acme"]
        },
        "name": {
          "type": "string",
          "title": "Component Name",
          "description": "The name of the component. This will often be a shortened, single name of the component. Examples: commons-lang3 and jquery",
          "examples": ["tomcat-catalina"]
        },
        "version": {
          "type": "string",
          "title": "Component Version",
          "description": "The component version. The version should ideally comply with semantic versioning but is not enforced.",
          "examples": ["9.0.14"]
        },
        "description": {
          "type": "string",
          "title": "Component Description",
          "description": "Specifies a description for the component"
        },
        "scope": {
          "type": "string",
          "enum": [
            "required",
            "optional",
            "excluded"
          ],
          "title": "Component Scope",
          "description": "Specifies the scope of the component. If scope is not specified, 'required' scope SHOULD be assumed by the consumer of the BOM.",
          "default": "required"
        },
        "hashes": {
          "type": "array",
          "title": "Component Hashes",
          "items": {"$ref": "#/definitions/hash"}
        },
        "licenses": {
          "$ref": "#/definitions/licenseChoice",
          "title": "Component License(s)"
        },
        "copyright": {
          "type": "string",
          "title": "Component Copyright",
          "description": "A copyright notice informing users of the underlying claims to copyright ownership in a published work.",
          "examples": ["Acme Inc"]
        },
        "cpe": {
          "type": "string",
          "title": "Component Common Platform Enumeration (CPE)",
          "description": "Specifies a well-formed CPE name that conforms to the CPE 2.2 or 2.3 specification. See [https://nvd.nist.gov/products/cpe](https://nvd.nist.gov/products/cpe)",
          "examples": ["cpe:2.3:a:acme:component_framework:-:*:*:*:*:*:*:*"]
        },
        "purl": {
          "type": "string",
          "title": "Component Package URL (purl)",
          "description": "Specifies the package-url (purl). The purl, if specified, MUST be valid and conform to the specification defined at: [https://github.com/package-url/purl-spec](https://github.com/package-url/purl-spec)",
          "examples": ["pkg:maven/com.acme/tomcat-catalina@9.0.14?packaging=jar"]
        },
        "swid": {
          "$ref": "#/definitions/swid",
          "title": "SWID Tag",
          "description": "Specifies metadata and content for [ISO-IEC 19770-2 Software Identification (SWID) Tags](https://www.iso.org/standard/65666.html)."
        },
        "modified": {
          "type": "boolean",
          "title": "Component Modified From Original",
          "description": "[Deprecated] - DO NOT USE. This will be removed in a future version. Use the pedigree element instead to supply information on exactly how the component was modified. A boolean value indicating if the component has been modified from the original. A value of true indicates the component is a derivative of the original. A value of false indicates the component has not been modified from the original."
        },
        "pedigree": {
          "type": "object",
          "title": "Component Pedigree",
          "description": "Component pedigree is a way to document complex supply chain scenarios where components are created, distributed, modified, redistributed, combined with other components, etc. Pedigree supports viewing this complex chain from the beginning, the end, or anywhere in the middle. It also provides a way to document variants where the exact relation may not be known.",
          "additionalProperties": false,
          "properties": {
            "ancestors": {
              "type": "array",
              "title": "Ancestors",
              "description": "Describes zero or more components in which a component is derived from. This is commonly used to describe forks from existing projects where the forked version contains a ancestor node containing the original component it was forked from. For example, Component A is the original component. Component B is the component being used and documented in the BOM. However, Component B contains a pedigree node with a single ancestor documenting Component A - the original component from which Component B is derived from.",
              "items": {"$ref": "#/definitions/component"}
            },
            "descendants": {
              "type": "array",
              "title": "Descendants",
              "description": "Descendants are the exact opposite of ancestors. This provides a way to document all forks (and their forks) of an original or root component.",
              "items": {"$ref": "#/definitions/component"}
            },
            "variants": {
              "type": "array",
              "title": "Variants",
              "description": "Variants describe relations where the relationship between the components are not known. For example, if Component A contains nearly identical code to Component B. They are both related, but it is unclear if one is derived from the other, or if they share a common ancestor.",
              "items": {"$ref": "#/definitions/component"}
            },
            "commits": {
              "type": "array",
              "title": "Commits",
              "description": "A list of zero or more commits which provide a trail describing how the component deviates from an ancestor, descendant, or variant.",
              "items": {"$ref": "#/definitions/commit"}
            },
            "patches": {
              "type": "array",
              "title": "Patches",
              "description": ">A list of zero or more patches describing how the component deviates from an ancestor, descendant, or variant. Patches may be complimentary to commits or may be used in place of commits.",
              "items": {"$ref": "#/definitions/patch"}
            },
            "notes": {
              "type": "string",
              "title": "Notes",
              "description": "Notes, observations, and other non-structured commentary describing the components pedigree."
            }
          }
        },
        "externalReferences": {
          "type": "array",
          "items": {"$ref": "#/definitions/externalReference"},
          "title": "External References",
          "description": "External references provide a way to document systems, sites, and information that may be relevant, but are not included with the BOM. They may also establish specific relationships within or external to the BOM."
        },
        "components": {
          "type": "array",
          "items": {"$ref": "#/definitions/component"},
          "uniqueItems": true,
          "title": "Components",
          "description": "A list of software and hardware components included in the parent component. This is not a dependency tree. It provides a way to specify a hierarchical representation of component assemblies, similar to system &#8594; subsystem &#8594; parts assembly in physical supply chains."
        },
        "evidence": {
          "$ref": "#/definitions/componentEvidence",
          "title": "Evidence",
          "description": "Provides the ability to document evidence collected through various forms of extraction or analysis."
        },
        "releaseNotes": {
          "$ref": "#/definitions/releaseNotes",
          "title": "Release notes",
          "description": "Specifies optional release notes."
        },
         "modelCard": {
          "$ref": "#/definitions/modelCard",
          "title": "Machine Learning Model Card"
        },
        "data": {
          "type": "array",
          "items": {"$ref": "#/definitions/componentData"},
          "title": "Data",
          "description": "This object SHOULD be specified for any component of type `data` and MUST NOT be specified for other component types."
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "description": "Provides the ability to document properties in a name-value store. This provides flexibility to include data not officially supported in the standard without having to use additional namespaces or create extensions. Unlike key-value stores, properties support duplicate names, each potentially having different values. Property names of interest to the general public are encouraged to be registered in the [CycloneDX Property Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy). Formal registration is OPTIONAL.",
          "items": {"$ref": "#/definitions/property"}
        },
        "signature": {
          "$ref": "#/definitions/signature",
          "title": "Signature",
          "description": "Enveloped signature in [JSON Signature Format (JSF)](https://cyberphone.github.io/doc/security/jsf.html)."
        }
      }
    },
    "swid": {
      "type": "object",
      "title": "SWID Tag",
      "description": "Specifies metadata and content for ISO-IEC 19770-2 Software Identification (SWID) Tags.",
      "required": [
        "tagId",
        "name"
      ],
      "additionalProperties": false,
      "properties": {
        "tagId": {
          "type": "string",
          "title": "Tag ID",
          "description": "Maps to the tagId of a SoftwareIdentity."
        },
        "name": {
          "type": "string",
          "title": "Name",
          "description": "Maps to the name of a SoftwareIdentity."
        },
        "version": {
          "type": "string",
          "title": "Version",
          "default": "0.0",
          "description": "Maps to the version of a SoftwareIdentity."
        },
        "tagVersion": {
          "type": "integer",
          "title": "Tag Version",
          "default": 0,
          "description": "Maps to the tagVersion of a SoftwareIdentity."
        },
        "patch": {
          "type": "boolean",
          "title": "Patch",
          "default": false,
          "description": "Maps to the patch of a SoftwareIdentity."
        },
        "text": {
          "title": "Attachment text",
          "description": "Specifies the metadata and content of the SWID tag.",
          "$ref": "#/definitions/attachment"
        },
        "url": {
          "type": "string",
          "title": "URL",
          "description": "The URL to the SWID file.",
          "format": "iri-reference"
        }
      }
    },
    "attachment": {
      "type": "object",
      "title": "Attachment",
      "description": "Specifies the metadata and content for an attachment.",
      "required": [
        "content"
      ],
      "additionalProperties": false,
      "properties": {
        "contentType": {
          "type": "string",
          "title": "Content-Type",
          "description": "Specifies the content type of the text. Defaults to text/plain if not specified.",
          "default": "text/plain"
        },
        "encoding": {
          "type": "string",
          "title": "Encoding",
          "description": "Specifies the optional encoding the text is represented in.",
          "enum": [
            "base64"
          ]
        },
        "content": {
          "type": "string",
          "title": "Attachment Text",
          "description": "The attachment data. Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text."
        }
      }
    },
    "hash": {
      "type": "object",
      "title": "Hash Objects",
      "required": [
        "alg",
        "content"
      ],
      "additionalProperties": false,
      "properties": {
        "alg": {
          "$ref": "#/definitions/hash-alg"
        },
        "content": {
          "$ref": "#/definitions/hash-content"
        }
      }
    },
    "hash-alg": {
      "type": "string",
      "enum": [
        "MD5",
        "SHA-1",
        "SHA-256",
        "SHA-384",
        "SHA-512",
        "SHA3-256",
        "SHA3-384",
        "SHA3-512",
        "BLAKE2b-256",
        "BLAKE2b-384",
        "BLAKE2b-512",
        "BLAKE3"
      ],
      "title": "Hash Algorithm"
    },
    "hash-content": {
      "type": "string",
      "title": "Hash Content (value)",
      "examples": ["3942447fac867ae5cdb3229b658f4d48"],
      "pattern": "^([a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64}|[a-fA-F0-9]{96}|[a-fA-F0-9]{128})$"
    },
    "license": {
      "type": "object",
      "title": "License Object",
      "oneOf": [
        {
          "required": ["id"]
        },
        {
          "required": ["name"]
        }
      ],
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "$ref": "#/definitions/refType",
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the license elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
        },
        "id": {
          "$ref": "spdx.schema.json",
          "title": "License ID (SPDX)",
          "description": "A valid SPDX license ID",
          "examples": ["Apache-2.0"]
        },
        "name": {
          "type": "string",
          "title": "License Name",
          "description": "If SPDX does not define the license used, this field may be used to provide the license name",
          "examples": ["Acme Software License"]
        },
        "text": {
          "title": "License text",
          "description": "An optional way to include the textual content of a license.",
          "$ref": "#/definitions/attachment"
        },
        "url": {
          "type": "string",
          "title": "License URL",
          "description": "The URL to the license file. If specified, a 'license' externalReference should also be specified for completeness",
          "examples": ["https://www.apache.org/licenses/LICENSE-2.0.txt"],
          "format": "iri-reference"
        },
        "licensing": {
          "type": "object",
          "title": "Licensing information",
          "description": "Licensing details describing the licensor/licensee, license type, renewal and expiration dates, and other important metadata",
          "additionalProperties": false,
          "properties": {
            "altIds": {
              "type": "array",
              "title": "Alternate License Identifiers",
              "description": "License identifiers that may be used to manage licenses and their lifecycle",
              "items": {
                "type": "string"
              }
            },
            "licensor": {
              "title": "Licensor",
              "description": "The individual or organization that grants a license to another individual or organization",
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "organization": {
                  "title": "Licensor (Organization)",
                  "description": "The organization that granted the license",
                  "$ref": "#/definitions/organizationalEntity"
                },
                "individual": {
                  "title": "Licensor (Individual)",
                  "description": "The individual, not associated with an organization, that granted the license",
                  "$ref": "#/definitions/organizationalContact"
                }
              },
              "oneOf":[
                {
                  "required": ["organization"]
                },
                {
                  "required": ["individual"]
                }
              ]
            },
            "licensee": {
              "title": "Licensee",
              "description": "The individual or organization for which a license was granted to",
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "organization": {
                  "title": "Licensee (Organization)",
                  "description": "The organization that was granted the license",
                  "$ref": "#/definitions/organizationalEntity"
                },
                "individual": {
                  "title": "Licensee (Individual)",
                  "description": "The individual, not associated with an organization, that was granted the license",
                  "$ref": "#/definitions/organizationalContact"
                }
              },
              "oneOf":[
                {
                  "required": ["organization"]
                },
                {
                  "required": ["individual"]
                }
              ]
            },
            "purchaser": {
              "title": "Purchaser",
              "description": "The individual or organization that purchased the license",
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "organization": {
                  "title": "Purchaser (Organization)",
                  "description": "The organization that purchased the license",
                  "$ref": "#/definitions/organizationalEntity"
                },
                "individual": {
                  "title": "Purchaser (Individual)",
                  "description": "The individual, not associated with an organization, that purchased the license",
                  "$ref": "#/definitions/organizationalContact"
                }
              },
              "oneOf":[
                {
                  "required": ["organization"]
                },
                {
                  "required": ["individual"]
                }
              ]
            },
            "purchaseOrder": {
              "type": "string",
              "title": "Purchase Order",
              "description": "The purchase order identifier the purchaser sent to a supplier or vendor to authorize a purchase"
            },
            "licenseTypes": {
              "type": "array",
              "title": "License Type",
              "description": "The type of license(s) that was granted to the licensee\n\n* __academic__ = A license that grants use of software solely for the purpose of education or research.\n* __appliance__ = A license covering use of software embedded in a specific piece of hardware.\n* __client-access__ = A Client Access License (CAL) allows client computers to access services provided by server software.\n* __concurrent-user__ = A Concurrent User license (aka floating license) limits the number of licenses for a software application and licenses are shared among a larger number of users.\n* __core-points__ = A license where the core of a computer's processor is assigned a specific number of points.\n* __custom-metric__ = A license for which consumption is measured by non-standard metrics.\n* __device__ = A license that covers a defined number of installations on computers and other types of devices.\n* __evaluation__ = A license that grants permission to install and use software for trial purposes.\n* __named-user__ = A license that grants access to the software to one or more pre-defined users.\n* __node-locked__ = A license that grants access to the software on one or more pre-defined computers or devices.\n* __oem__ = An Original Equipment Manufacturer license that is delivered with hardware, cannot be transferred to other hardware, and is valid for the life of the hardware.\n* __perpetual__ = A license where the software is sold on a one-time basis and the licensee can use a copy of the software indefinitely.\n* __processor-points__ = A license where each installation consumes points per processor.\n* __subscription__ = A license where the licensee pays a fee to use the software or service.\n* __user__ = A license that grants access to the software or service by a specified number of users.\n* __other__ = Another license type.\n",
              "items": {
                "type": "string",
                "enum": [
                  "academic",
                  "appliance",
                  "client-access",
                  "concurrent-user",
                  "core-points",
                  "custom-metric",
                  "device",
                  "evaluation",
                  "named-user",
                  "node-locked",
                  "oem",
                  "perpetual",
                  "processor-points",
                  "subscription",
                  "user",
                  "other"
                ]
              }
            },
            "lastRenewal": {
              "type": "string",
              "format": "date-time",
              "title": "Last Renewal",
              "description": "The timestamp indicating when the license was last renewed. For new purchases, this is often the purchase or acquisition date. For non-perpetual licenses or subscriptions, this is the timestamp of when the license was last renewed."
            },
            "expiration": {
              "type": "string",
              "format": "date-time",
              "title": "Expiration",
              "description": "The timestamp indicating when the current license expires (if applicable)."
            }
          }
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "description": "Provides the ability to document properties in a name-value store. This provides flexibility to include data not officially supported in the standard without having to use additional namespaces or create extensions. Unlike key-value stores, properties support duplicate names, each potentially having different values. Property names of interest to the general public are encouraged to be registered in the [CycloneDX Property Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy). Formal registration is OPTIONAL.",
          "items": {"$ref": "#/definitions/property"}
        }
      }
    },
    "licenseChoice": {
      "title": "License Choice",
      "description": "EITHER (list of SPDX licenses and/or named licenses) OR (tuple of one SPDX License Expression)",
      "type": "array",
      "oneOf": [
        {
          "title": "Multiple licenses",
          "description": "A list of SPDX licenses and/or named licenses.",
          "type": "array",
          "items": {
            "type": "object",
            "required": ["license"],
            "additionalProperties": false,
            "properties": {
              "license": {"$ref": "#/definitions/license"}
            }
          }
        },
        {
          "title": "SPDX License Expression",
          "description": "A tuple of exactly one SPDX License Expression.",
          "type": "array",
          "additionalItems": false,
          "minItems": 1,
          "maxItems": 1,
          "items": [{
            "type": "object",
            "additionalProperties": false,
            "required": ["expression"],
            "properties": {
              "expression": {
                "type": "string",
                "title": "SPDX License Expression",
                "examples": [
                  "Apache-2.0 AND (MIT OR GPL-2.0-only)",
                  "GPL-3.0-only WITH Classpath-exception-2.0"
                ]
              },
              "bom-ref": {
                "$ref": "#/definitions/refType",
                "title": "BOM Reference",
                "description": "An optional identifier which can be used to reference the license elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
              }
            }
          }]
        }
      ]
    },
    "commit": {
      "type": "object",
      "title": "Commit",
      "description": "Specifies an individual commit",
      "additionalProperties": false,
      "properties": {
        "uid": {
          "type": "string",
          "title": "UID",
          "description": "A unique identifier of the commit. This may be version control specific. For example, Subversion uses revision numbers whereas git uses commit hashes."
        },
        "url": {
          "type": "string",
          "title": "URL",
          "description": "The URL to the commit. This URL will typically point to a commit in a version control system.",
          "format": "iri-reference"
        },
        "author": {
          "title": "Author",
          "description": "The author who created the changes in the commit",
          "$ref": "#/definitions/identifiableAction"
        },
        "committer": {
          "title": "Committer",
          "description": "The person who committed or pushed the commit",
          "$ref": "#/definitions/identifiableAction"
        },
        "message": {
          "type": "string",
          "title": "Message",
          "description": "The text description of the contents of the commit"
        }
      }
    },
    "patch": {
      "type": "object",
      "title": "Patch",
      "description": "Specifies an individual patch",
      "required": [
        "type"
      ],
      "additionalProperties": false,
      "properties": {
        "type": {
          "type": "string",
          "enum": [
            "unofficial",
            "monkey",
            "backport",
            "cherry-pick"
          ],
          "title": "Type",
          "description": "Specifies the purpose for the patch including the resolution of defects, security issues, or new behavior or functionality.\n\n* __unofficial__ = A patch which is not developed by the creators or maintainers of the software being patched. Refer to [https://en.wikipedia.org/wiki/Unofficial_patch](https://en.wikipedia.org/wiki/Unofficial_patch)\n* __monkey__ = A patch which dynamically modifies runtime behavior. Refer to [https://en.wikipedia.org/wiki/Monkey_patch](https://en.wikipedia.org/wiki/Monkey_patch)\n* __backport__ = A patch which takes code from a newer version of software and applies it to older versions of the same software. Refer to [https://en.wikipedia.org/wiki/Backporting](https://en.wikipedia.org/wiki/Backporting)\n* __cherry-pick__ = A patch created by selectively applying commits from other versions or branches of the same software."
        },
        "diff": {
          "title": "Diff",
          "description": "The patch file (or diff) that show changes. Refer to [https://en.wikipedia.org/wiki/Diff](https://en.wikipedia.org/wiki/Diff)",
          "$ref": "#/definitions/diff"
        },
        "resolves": {
          "type": "array",
          "items": {"$ref": "#/definitions/issue"},
          "title": "Resolves",
          "description": "A collection of issues the patch resolves"
        }
      }
    },
    "diff": {
      "type": "object",
      "title": "Diff",
      "description": "The patch file (or diff) that show changes. Refer to https://en.wikipedia.org/wiki/Diff",
      "additionalProperties": false,
      "properties": {
        "text": {
          "title": "Diff text",
          "description": "Specifies the optional text of the diff",
          "$ref": "#/definitions/attachment"
        },
        "url": {
          "type": "string",
          "title": "URL",
          "description": "Specifies the URL to the diff",
          "format": "iri-reference"
        }
      }
    },
    "issue": {
      "type": "object",
      "title": "Diff",
      "description": "An individual issue that has been resolved.",
      "required": [
        "type"
      ],
      "additionalProperties": false,
      "properties": {
        "type": {
          "type": "string",
          "enum": [
            "defect",
            "enhancement",
            "security"
          ],
          "title": "Type",
          "description": "Specifies the type of issue"
        },
        "id": {
          "type": "string",
          "title": "ID",
          "description": "The identifier of the issue assigned by the source of the issue"
        },
        "name": {
          "type": "string",
          "title": "Name",
          "description": "The name of the issue"
        },
        "description": {
          "type": "string",
          "title": "Description",
          "description": "A description of the issue"
        },
        "source": {
          "type": "object",
          "title": "Source",
          "description": "The source of the issue where it is documented",
          "additionalProperties": false,
          "properties": {
            "name": {
              "type": "string",
              "title": "Name",
              "description": "The name of the source. For example 'National Vulnerability Database', 'NVD', and 'Apache'"
            },
            "url": {
              "type": "string",
              "title": "URL",
              "description": "The url of the issue documentation as provided by the source",
              "format": "iri-reference"
            }
          }
        },
        "references": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "iri-reference"
          },
          "title": "References",
          "description": "A collection of URL's for reference. Multiple URLs are allowed.",
          "examples": ["https://example.com"]
        }
      }
    },
    "identifiableAction": {
      "type": "object",
      "title": "Identifiable Action",
      "description": "Specifies an individual commit",
      "additionalProperties": false,
      "properties": {
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "title": "Timestamp",
          "description": "The timestamp in which the action occurred"
        },
        "name": {
          "type": "string",
          "title": "Name",
          "description": "The name of the individual who performed the action"
        },
        "email": {
          "type": "string",
          "format": "idn-email",
          "title": "E-mail",
          "description": "The email address of the individual who performed the action"
        }
      }
    },
    "externalReference": {
      "type": "object",
      "title": "External Reference",
      "description": "External references provide a way to document systems, sites, and information that may be relevant, but are not included with the BOM. They may also establish specific relationships within or external to the BOM.",
      "required": [
        "url",
        "type"
      ],
      "additionalProperties": false,
      "properties": {
        "url": {
          "anyOf": [
            {
              "title": "URL",
              "type": "string",
              "format": "iri-reference"
            },
            {
              "title": "BOM-Link",
              "$ref": "#/definitions/bomLink"
            }
          ],
          "title": "URL",
          "description": "The URI (URL or URN) to the external reference. External references are URIs and therefore can accept any URL scheme including https ([RFC-7230](https://www.ietf.org/rfc/rfc7230.txt)), mailto ([RFC-2368](https://www.ietf.org/rfc/rfc2368.txt)), tel ([RFC-3966](https://www.ietf.org/rfc/rfc3966.txt)), and dns ([RFC-4501](https://www.ietf.org/rfc/rfc4501.txt)). External references may also include formally registered URNs such as [CycloneDX BOM-Link](https://cyclonedx.org/capabilities/bomlink/) to reference CycloneDX BOMs or any object within a BOM. BOM-Link transforms applicable external references into relationships that can be expressed in a BOM or across BOMs."
        },
        "comment": {
          "type": "string",
          "title": "Comment",
          "description": "An optional comment describing the external reference"
        },
        "type": {
          "type": "string",
          "title": "Type",
          "description": "Specifies the type of external reference.\n\n* __vcs__ = Version Control System\n* __issue-tracker__ = Issue or defect tracking system, or an Application Lifecycle Management (ALM) system\n* __website__ = Website\n* __advisories__ = Security advisories\n* __bom__ = Bill of Materials (SBOM, OBOM, HBOM, SaaSBOM, etc)\n* __mailing-list__ = Mailing list or discussion group\n* __social__ = Social media account\n* __chat__ = Real-time chat platform\n* __documentation__ = Documentation, guides, or how-to instructions\n* __support__ = Community or commercial support\n* __distribution__ = Direct or repository download location\n* __distribution-intake__ = The location where a component was published to. This is often the same as \"distribution\" but may also include specialized publishing processes that act as an intermediary\n* __license__ = The URL to the license file. If a license URL has been defined in the license node, it should also be defined as an external reference for completeness\n* __build-meta__ = Build-system specific meta file (i.e. pom.xml, package.json, .nuspec, etc)\n* __build-system__ = URL to an automated build system\n* __release-notes__ = URL to release notes\n* __security-contact__ = Specifies a way to contact the maintainer, supplier, or provider in the event of a security incident. Common URIs include links to a disclosure procedure, a mailto (RFC-2368) that specifies an email address, a tel (RFC-3966) that specifies a phone number, or dns (RFC-4501) that specifies the records containing DNS Security TXT\n* __model-card__ = A model card describes the intended uses of a machine learning model, potential limitations, biases, ethical considerations, training parameters, datasets used to train the model, performance metrics, and other relevant data useful for ML transparency\n* __log__ = A record of events that occurred in a computer system or application, such as problems, errors, or information on current operations\n* __configuration__ = Parameters or settings that may be used by other components or services\n* __evidence__ = Information used to substantiate a claim\n* __formulation__ = Describes how a component or service was manufactured or deployed\n* __attestation__ = Human or machine-readable statements containing facts, evidence, or testimony\n* __threat-model__ = An enumeration of identified weaknesses, threats, and countermeasures, dataflow diagram (DFD), attack tree, and other supporting documentation in human-readable or machine-readable format\n* __adversary-model__ = The defined assumptions, goals, and capabilities of an adversary.\n* __risk-assessment__ = Identifies and analyzes the potential of future events that may negatively impact individuals, assets, and/or the environment. Risk assessments may also include judgments on the tolerability of each risk.\n* __vulnerability-assertion__ = A Vulnerability Disclosure Report (VDR) which asserts the known and previously unknown vulnerabilities that affect a component, service, or product including the analysis and findings describing the impact (or lack of impact) that the reported vulnerability has on a component, service, or product.\n* __exploitability-statement__ = A Vulnerability Exploitability eXchange (VEX) which asserts the known vulnerabilities that do not affect a product, product family, or organization, and optionally the ones that do. The VEX should include the analysis and findings describing the impact (or lack of impact) that the reported vulnerability has on the product, product family, or organization.\n* __pentest-report__ = Results from an authorized simulated cyberattack on a component or service, otherwise known as a penetration test\n* __static-analysis-report__ = SARIF or proprietary machine or human-readable report for which static analysis has identified code quality, security, and other potential issues with the source code\n* __dynamic-analysis-report__ = Dynamic analysis report that has identified issues such as vulnerabilities and misconfigurations\n* __runtime-analysis-report__ = Report generated by analyzing the call stack of a running application\n* __component-analysis-report__ = Report generated by Software Composition Analysis (SCA), container analysis, or other forms of component analysis\n* __maturity-report__ = Report containing a formal assessment of an organization, business unit, or team against a maturity model\n* __certification-report__ = Industry, regulatory, or other certification from an accredited (if applicable) certification body\n* __quality-metrics__ = Report or system in which quality metrics can be obtained\n* __codified-infrastructure__ = Code or configuration that defines and provisions virtualized infrastructure, commonly referred to as Infrastructure as Code (IaC)\n* __poam__ = Plans of Action and Milestones (POAM) compliment an \"attestation\" external reference. POAM is defined by NIST as a \"document that identifies tasks needing to be accomplished. It details resources required to accomplish the elements of the plan, any milestones in meeting the tasks and scheduled completion dates for the milestones\".\n* __other__ = Use this if no other types accurately describe the purpose of the external reference",
          "enum": [
            "vcs",
            "issue-tracker",
            "website",
            "advisories",
            "bom",
            "mailing-list",
            "social",
            "chat",
            "documentation",
            "support",
            "distribution",
            "distribution-intake",
            "license",
            "build-meta",
            "build-system",
            "release-notes",
            "security-contact",
            "model-card",
            "log",
            "configuration",
            "evidence",
            "formulation",
            "attestation",
            "threat-model",
            "adversary-model",
            "risk-assessment",
            "vulnerability-assertion",
            "exploitability-statement",
            "pentest-report",
            "static-analysis-report",
            "dynamic-analysis-report",
            "runtime-analysis-report",
            "component-analysis-report",
            "maturity-report",
            "certification-report",
            "codified-infrastructure",
            "quality-metrics",
            "poam",
            "other"
          ]
        },
        "hashes": {
          "type": "array",
          "items": {"$ref": "#/definitions/hash"},
          "title": "Hashes",
          "description": "The hashes of the external reference (if applicable)."
        }
      }
    },
    "dependency": {
      "type": "object",
      "title": "Dependency",
      "description": "Defines the direct dependencies of a component or service. Components or services that do not have their own dependencies MUST be declared as empty elements within the graph. Components or services that are not represented in the dependency graph MAY have unknown dependencies. It is RECOMMENDED that implementations assume this to be opaque and not an indicator of a object being dependency-free. It is RECOMMENDED to leverage compositions to indicate unknown dependency graphs.",
      "required": [
        "ref"
      ],
      "additionalProperties": false,
      "properties": {
        "ref": {
          "$ref": "#/definitions/refLinkType",
          "title": "Reference",
          "description": "References a component or service by its bom-ref attribute"
        },
        "dependsOn": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/refLinkType"
          },
          "title": "Depends On",
          "description": "The bom-ref identifiers of the components or services that are dependencies of this dependency object."
        }
      }
    },
    "service": {
      "type": "object",
      "title": "Service Object",
      "required": [
        "name"
      ],
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "$ref": "#/definitions/refType",
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the service elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
        },
        "provider": {
          "title": "Provider",
          "description": "The organization that provides the service.",
          "$ref": "#/definitions/organizationalEntity"
        },
        "group": {
          "type": "string",
          "title": "Service Group",
          "description": "The grouping name, namespace, or identifier. This will often be a shortened, single name of the company or project that produced the service or domain name. Whitespace and special characters should be avoided.",
          "examples": ["com.acme"]
        },
        "name": {
          "type": "string",
          "title": "Service Name",
          "description": "The name of the service. This will often be a shortened, single name of the service.",
          "examples": ["ticker-service"]
        },
        "version": {
          "type": "string",
          "title": "Service Version",
          "description": "The service version.",
          "examples": ["1.0.0"]
        },
        "description": {
          "type": "string",
          "title": "Service Description",
          "description": "Specifies a description for the service"
        },
        "endpoints": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "iri-reference"
          },
          "title": "Endpoints",
          "description": "The endpoint URIs of the service. Multiple endpoints are allowed.",
          "examples": ["https://example.com/api/v1/ticker"]
        },
        "authenticated": {
          "type": "boolean",
          "title": "Authentication Required",
          "description": "A boolean value indicating if the service requires authentication. A value of true indicates the service requires authentication prior to use. A value of false indicates the service does not require authentication."
        },
        "x-trust-boundary": {
          "type": "boolean",
          "title": "Crosses Trust Boundary",
          "description": "A boolean value indicating if use of the service crosses a trust zone or boundary. A value of true indicates that by using the service, a trust boundary is crossed. A value of false indicates that by using the service, a trust boundary is not crossed."
        },
        "trustZone": {
          "type": "string",
          "title": "Trust Zone",
          "description": "The name of the trust zone the service resides in."
        },
        "data": {
          "type": "array",
          "items": {"$ref": "#/definitions/serviceData"},
          "title": "Data",
          "description": "Specifies information about the data including the directional flow of data and the data classification."
        },
        "licenses": {
          "$ref": "#/definitions/licenseChoice",
          "title": "Component License(s)"
        },
        "externalReferences": {
          "type": "array",
          "items": {"$ref": "#/definitions/externalReference"},
          "title": "External References",
          "description": "External references provide a way to document systems, sites, and information that may be relevant, but are not included with the BOM. They may also establish specific relationships within or external to the BOM."
        },
        "services": {
          "type": "array",
          "items": {"$ref": "#/definitions/service"},
          "uniqueItems": true,
          "title": "Services",
          "description": "A list of services included or deployed behind the parent service. This is not a dependency tree. It provides a way to specify a hierarchical representation of service assemblies."
        },
        "releaseNotes": {
          "$ref": "#/definitions/releaseNotes",
          "title": "Release notes",
          "description": "Specifies optional release notes."
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "description": "Provides the ability to document properties in a name-value store. This provides flexibility to include data not officially supported in the standard without having to use additional namespaces or create extensions. Unlike key-value stores, properties support duplicate names, each potentially having different values. Property names of interest to the general public are encouraged to be registered in the [CycloneDX Property Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy). Formal registration is OPTIONAL.",
          "items": {"$ref": "#/definitions/property"}
        },
        "signature": {
          "$ref": "#/definitions/signature",
          "title": "Signature",
          "description": "Enveloped signature in [JSON Signature Format (JSF)](https://cyberphone.github.io/doc/security/jsf.html)."
        }
      }
    },
    "serviceData": {
      "type": "object",
      "title": "Hash Objects",
      "required": [
        "flow",
        "classification"
      ],
      "additionalProperties": false,
      "properties": {
        "flow": {
          "$ref": "#/definitions/dataFlowDirection",
          "title": "Directional Flow",
          "description": "Specifies the flow direction of the data. Direction is relative to the service. Inbound flow states that data enters the service. Outbound flow states that data leaves the service. Bi-directional states that data flows both ways, and unknown states that the direction is not known."
        },
        "classification": {
          "$ref": "#/definitions/dataClassification"
        },
        "name": {
          "type": "string",
          "title": "Name",
          "description": "Name for the defined data",
          "examples": [
            "Credit card reporting"
          ]
        },
        "description": {
          "type": "string",
          "title": "Description",
          "description": "Short description of the data content and usage",
          "examples": [
            "Credit card information being exchanged in between the web app and the database"
          ]
        },
        "governance": {
          "type": "object",
          "title": "Data Governance",
          "$ref": "#/definitions/dataGovernance"
        },
        "source": {
          "type": "array",
          "items": {
            "anyOf": [
              {
                "title": "URL",
                "type": "string",
                "format": "iri-reference"
              },
              {
                "title": "BOM-Link Element",
                "$ref": "#/definitions/bomLinkElementType"
              }
            ]
          },
          "title": "Source",
          "description": "The URI, URL, or BOM-Link of the components or services the data came in from"
        },
        "destination": {
          "type": "array",
          "items": {
            "anyOf": [
              {
                "title": "URL",
                "type": "string",
                "format": "iri-reference"
              },
              {
                "title": "BOM-Link Element",
                "$ref": "#/definitions/bomLinkElementType"
              }
            ]
          },
          "title": "Destination",
          "description": "The URI, URL, or BOM-Link of the components or services the data is sent to"
        }
      }
    },
    "dataFlowDirection": {
      "type": "string",
      "enum": [
        "inbound",
        "outbound",
        "bi-directional",
        "unknown"
      ],
      "title": "Data flow direction",
      "description": "Specifies the flow direction of the data. Direction is relative to the service. Inbound flow states that data enters the service. Outbound flow states that data leaves the service. Bi-directional states that data flows both ways, and unknown states that the direction is not known."
    },

    "copyright": {
      "type": "object",
      "title": "Copyright",
      "required": [
        "text"
      ],
      "additionalProperties": false,
      "properties": {
        "text": {
          "type": "string",
          "title": "Copyright Text"
        }
      }
    },
    "componentEvidence": {
      "type": "object",
      "title": "Evidence",
      "description": "Provides the ability to document evidence collected through various forms of extraction or analysis.",
      "additionalProperties": false,
      "properties": {
        "identity": {
          "type": "object",
          "description": "Evidence that substantiates the identity of a component.",
          "required": [ "field" ],
          "additionalProperties": false,
          "properties": {
            "field": {
              "type": "string",
              "enum": [
                "group", "name", "version", "purl", "cpe", "swid", "hash"
              ],
              "title": "Field",
              "description": "The identity field of the component which the evidence describes."
            },
            "confidence": {
              "type": "number",
              "minimum": 0,
              "maximum": 1,
              "title": "Confidence",
              "description": "The overall confidence of the evidence from 0 - 1, where 1 is 100% confidence."
            },
            "methods": {
              "type": "array",
              "title": "Methods",
              "description": "The methods used to extract and/or analyze the evidence.",
              "items": {
                "type": "object",
                "required": [
                  "technique" ,
                  "confidence"
                ],
                "additionalProperties": false,
                "properties": {
                  "technique": {
                    "title": "Technique",
                    "description": "The technique used in this method of analysis.",
                    "type": "string",
                    "enum": [
                      "source-code-analysis",
                      "binary-analysis",
                      "manifest-analysis",
                      "ast-fingerprint",
                      "hash-comparison",
                      "instrumentation",
                      "dynamic-analysis",
                      "filename",
                      "attestation",
                      "other"
                    ]
                  },
                  "confidence": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "title": "Confidence",
                    "description": "The confidence of the evidence from 0 - 1, where 1 is 100% confidence. Confidence is specific to the technique used. Each technique of analysis can have independent confidence."
                  },
                  "value": {
                    "type": "string",
                    "title": "Value",
                    "description": "The value or contents of the evidence."
                  }
                }
              }
            },
            "tools": {
              "type": "array",
              "uniqueItems": true,
              "items": {
                "anyOf": [
                  {
                    "title": "Ref",
                    "$ref": "#/definitions/refLinkType"
                  },
                  {
                    "title": "BOM-Link Element",
                    "$ref": "#/definitions/bomLinkElementType"
                  }
                ]
              },
              "title": "BOM References",
              "description": "The object in the BOM identified by its bom-ref. This is often a component or service, but may be any object type supporting bom-refs. Tools used for analysis should already be defined in the BOM, either in the metadata/tools, components, or formulation."
            }
          }
        },
        "occurrences": {
          "type": "array",
          "title": "Occurrences",
          "description": "Evidence of individual instances of a component spread across multiple locations.",
          "items": {
            "type": "object",
            "required": [ "location" ],
            "additionalProperties": false,
            "properties": {
              "bom-ref": {
                "$ref": "#/definitions/refType",
                "title": "BOM Reference",
                "description": "An optional identifier which can be used to reference the occurrence elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
              },
              "location": {
                "type": "string",
                "title": "Location",
                "description": "The location or path to where the component was found."
              }
            }
          }
        },
        "callstack": {
          "type": "object",
          "description": "Evidence of the components use through the callstack.",
          "additionalProperties": false,
          "properties": {
            "frames": {
              "type": "array",
              "title": "Methods",
              "items": {
                "type": "object",
                "required": [
                  "module"
                ],
                "additionalProperties": false,
                "properties": {
                  "package": {
                    "title": "Package",
                    "description": "A package organizes modules into namespaces, providing a unique namespace for each type it contains.",
                    "type": "string"
                  },
                  "module": {
                    "title": "Module",
                    "description": "A module or class that encloses functions/methods and other code.",
                    "type": "string"
                  },
                  "function": {
                    "title": "Function",
                    "description": "A block of code designed to perform a particular task.",
                    "type": "string"
                  },
                  "parameters": {
                    "title": "Parameters",
                    "description": "Optional arguments that are passed to the module or function.",
                    "type": "array",
                    "items": {
                      "type": "string"
                    }
                  },
                  "line": {
                    "title": "Line",
                    "description": "The line number the code that is called resides on.",
                    "type": "integer"
                  },
                  "column": {
                    "title": "Column",
                    "description": "The column the code that is called resides.",
                    "type": "integer"
                  },
                  "fullFilename": {
                    "title": "Full Filename",
                    "description": "The full path and filename of the module.",
                    "type": "string"
                  }
                }
              }
            }
          }
        },
        "licenses": {
          "$ref": "#/definitions/licenseChoice",
          "title": "Component License(s)"
        },
        "copyright": {
          "type": "array",
          "items": {"$ref": "#/definitions/copyright"},
          "title": "Copyright"
        }
      }
    },
    "compositions": {
      "type": "object",
      "title": "Compositions",
      "required": [
        "aggregate"
      ],
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "$ref": "#/definitions/refType",
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the composition elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
        },
        "aggregate": {
          "$ref": "#/definitions/aggregateType",
          "title": "Aggregate",
          "description": "Specifies an aggregate type that describe how complete a relationship is.\n\n* __complete__ = The relationship is complete. No further relationships including constituent components, services, or dependencies are known to exist.\n* __incomplete__ = The relationship is incomplete. Additional relationships exist and may include constituent components, services, or dependencies.\n* __incomplete&#95;first&#95;party&#95;only__ = The relationship is incomplete. Only relationships for first-party components, services, or their dependencies are represented.\n* __incomplete&#95;first&#95;party&#95;proprietary&#95;only__ = The relationship is incomplete. Only relationships for first-party components, services, or their dependencies are represented, limited specifically to those that are proprietary.\n* __incomplete&#95;first&#95;party&#95;opensource&#95;only__ = The relationship is incomplete. Only relationships for first-party components, services, or their dependencies are represented, limited specifically to those that are opensource.\n* __incomplete&#95;third&#95;party&#95;only__ = The relationship is incomplete. Only relationships for third-party components, services, or their dependencies are represented.\n* __incomplete&#95;third&#95;party&#95;proprietary&#95;only__ = The relationship is incomplete. Only relationships for third-party components, services, or their dependencies are represented, limited specifically to those that are proprietary.\n* __incomplete&#95;third&#95;party&#95;opensource&#95;only__ = The relationship is incomplete. Only relationships for third-party components, services, or their dependencies are represented, limited specifically to those that are opensource.\n* __unknown__ = The relationship may be complete or incomplete. This usually signifies a 'best-effort' to obtain constituent components, services, or dependencies but the completeness is inconclusive.\n* __not&#95;specified__ = The relationship completeness is not specified.\n"
        },
        "assemblies": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "anyOf": [
              {
                "title": "Ref",
                "$ref": "#/definitions/refLinkType"
              },
              {
                "title": "BOM-Link Element",
                "$ref": "#/definitions/bomLinkElementType"
              }
            ]
          },
          "title": "BOM references",
          "description": "The bom-ref identifiers of the components or services being described. Assemblies refer to nested relationships whereby a constituent part may include other constituent parts. References do not cascade to child parts. References are explicit for the specified constituent part only."
        },
        "dependencies": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "type": "string"
          },
          "title": "BOM references",
          "description": "The bom-ref identifiers of the components or services being described. Dependencies refer to a relationship whereby an independent constituent part requires another independent constituent part. References do not cascade to transitive dependencies. References are explicit for the specified dependency only."
        },
        "vulnerabilities": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "type": "string"
          },
          "title": "BOM references",
          "description": "The bom-ref identifiers of the vulnerabilities being described."
        },
        "signature": {
          "$ref": "#/definitions/signature",
          "title": "Signature",
          "description": "Enveloped signature in [JSON Signature Format (JSF)](https://cyberphone.github.io/doc/security/jsf.html)."
        }
      }
    },
    "aggregateType": {
      "type": "string",
      "default": "not_specified",
      "enum": [
        "complete",
        "incomplete",
        "incomplete_first_party_only",
        "incomplete_first_party_proprietary_only",
        "incomplete_first_party_opensource_only",
        "incomplete_third_party_only",
        "incomplete_third_party_proprietary_only",
        "incomplete_third_party_opensource_only",
        "unknown",
        "not_specified"
      ]
    },
    "property": {
      "type": "object",
      "title": "Lightweight name-value pair",
      "description": "Provides the ability to document properties in a name-value store. This provides flexibility to include data not officially supported in the standard without having to use additional namespaces or create extensions. Unlike key-value stores, properties support duplicate names, each potentially having different values. Property names of interest to the general public are encouraged to be registered in the [CycloneDX Property Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy). Formal registration is OPTIONAL.",
      "properties": {
        "name": {
          "type": "string",
          "title": "Name",
          "description": "The name of the property. Duplicate names are allowed, each potentially having a different value."
        },
        "value": {
          "type": "string",
          "title": "Value",
          "description": "The value of the property."
        }
      }
    },
    "localeType": {
      "type": "string",
      "pattern": "^([a-z]{2})(-[A-Z]{2})?$",
      "title": "Locale",
      "description": "Defines a syntax for representing two character language code (ISO-639) followed by an optional two character country code. The language code MUST be lower case. If the country code is specified, the country code MUST be upper case. The language code and country code MUST be separated by a minus sign. Examples: en, en-US, fr, fr-CA"
    },
    "releaseType": {
      "type": "string",
      "examples": [
        "major",
        "minor",
        "patch",
        "pre-release",
        "internal"
      ],
      "description": "The software versioning type. It is RECOMMENDED that the release type use one of 'major', 'minor', 'patch', 'pre-release', or 'internal'. Representing all possible software release types is not practical, so standardizing on the recommended values, whenever possible, is strongly encouraged.\n\n* __major__ = A major release may contain significant changes or may introduce breaking changes.\n* __minor__ = A minor release, also known as an update, may contain a smaller number of changes than major releases.\n* __patch__ = Patch releases are typically unplanned and may resolve defects or important security issues.\n* __pre-release__ = A pre-release may include alpha, beta, or release candidates and typically have limited support. They provide the ability to preview a release prior to its general availability.\n* __internal__ = Internal releases are not for public consumption and are intended to be used exclusively by the project or manufacturer that produced it."
    },
    "note": {
      "type": "object",
      "title": "Note",
      "description": "A note containing the locale and content.",
      "required": [
        "text"
      ],
      "additionalProperties": false,
      "properties": {
        "locale": {
          "$ref": "#/definitions/localeType",
          "title": "Locale",
          "description": "The ISO-639 (or higher) language code and optional ISO-3166 (or higher) country code. Examples include: \"en\", \"en-US\", \"fr\" and \"fr-CA\""
        },
        "text": {
          "title": "Release note content",
          "description": "Specifies the full content of the release note.",
          "$ref": "#/definitions/attachment"
        }
      }
    },
    "releaseNotes": {
      "type": "object",
      "title": "Release notes",
      "required": [
        "type"
      ],
      "additionalProperties": false,
      "properties": {
        "type": {
          "$ref": "#/definitions/releaseType",
          "title": "Type",
          "description": "The software versioning type the release note describes."
        },
        "title": {
          "type": "string",
          "title": "Title",
          "description": "The title of the release."
        },
        "featuredImage": {
          "type": "string",
          "format": "iri-reference",
          "title": "Featured image",
          "description": "The URL to an image that may be prominently displayed with the release note."
        },
        "socialImage": {
          "type": "string",
          "format": "iri-reference",
          "title": "Social image",
          "description": "The URL to an image that may be used in messaging on social media platforms."
        },
        "description": {
          "type": "string",
          "title": "Description",
          "description": "A short description of the release."
        },
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "title": "Timestamp",
          "description": "The date and time (timestamp) when the release note was created."
        },
        "aliases": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "title": "Aliases",
          "description": "One or more alternate names the release may be referred to. This may include unofficial terms used by development and marketing teams (e.g. code names)."
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "title": "Tags",
          "description": "One or more tags that may aid in search or retrieval of the release note."
        },
        "resolves": {
          "type": "array",
          "items": {"$ref": "#/definitions/issue"},
          "title": "Resolves",
          "description": "A collection of issues that have been resolved."
        },
        "notes": {
          "type": "array",
          "items": {"$ref": "#/definitions/note"},
          "title": "Notes",
          "description": "Zero or more release notes containing the locale and content. Multiple note objects may be specified to support release notes in a wide variety of languages."
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "description": "Provides the ability to document properties in a name-value store. This provides flexibility to include data not officially supported in the standard without having to use additional namespaces or create extensions. Unlike key-value stores, properties support duplicate names, each potentially having different values. Property names of interest to the general public are encouraged to be registered in the [CycloneDX Property Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy). Formal registration is OPTIONAL.",
          "items": {"$ref": "#/definitions/property"}
        }
      }
    },
    "advisory": {
      "type": "object",
      "title": "Advisory",
      "description": "Title and location where advisory information can be obtained. An advisory is a notification of a threat to a component, service, or system.",
      "required": ["url"],
      "additionalProperties": false,
      "properties": {
        "title": {
          "type": "string",
          "title": "Title",
          "description": "An optional name of the advisory."
        },
        "url": {
          "type": "string",
          "title": "URL",
          "format": "iri-reference",
          "description": "Location where the advisory can be obtained."
        }
      }
    },
    "cwe": {
      "type": "integer",
      "minimum": 1,
      "title": "CWE",
      "description": "Integer representation of a Common Weaknesses Enumerations (CWE). For example 399 (of https://cwe.mitre.org/data/definitions/399.html)"
    },
    "severity": {
      "type": "string",
      "title": "Severity",
      "description": "Textual representation of the severity of the vulnerability adopted by the analysis method. If the analysis method uses values other than what is provided, the user is expected to translate appropriately.",
      "enum": [
        "critical",
        "high",
        "medium",
        "low",
        "info",
        "none",
        "unknown"
      ]
    },
    "scoreMethod": {
      "type": "string",
      "title": "Method",
      "description": "Specifies the severity or risk scoring methodology or standard used.\n\n* CVSSv2 - [Common Vulnerability Scoring System v2](https://www.first.org/cvss/v2/)\n* CVSSv3 - [Common Vulnerability Scoring System v3](https://www.first.org/cvss/v3-0/)\n* CVSSv31 - [Common Vulnerability Scoring System v3.1](https://www.first.org/cvss/v3-1/)\n* CVSSv4 - [Common Vulnerability Scoring System v4](https://www.first.org/cvss/v4-0/)\n* OWASP - [OWASP Risk Rating Methodology](https://owasp.org/www-community/OWASP_Risk_Rating_Methodology)\n* SSVC - [Stakeholder Specific Vulnerability Categorization](https://github.com/CERTCC/SSVC) (all versions)",
      "enum": [
        "CVSSv2",
        "CVSSv3",
        "CVSSv31",
        "CVSSv4",
        "OWASP",
        "SSVC",
        "other"
      ]
    },
    "impactAnalysisState": {
      "type": "string",
      "title": "Impact Analysis State",
      "description": "Declares the current state of an occurrence of a vulnerability, after automated or manual analysis. \n\n* __resolved__ = the vulnerability has been remediated. \n* __resolved\\_with\\_pedigree__ = the vulnerability has been remediated and evidence of the changes are provided in the affected components pedigree containing verifiable commit history and/or diff(s). \n* __exploitable__ = the vulnerability may be directly or indirectly exploitable. \n* __in\\_triage__ = the vulnerability is being investigated. \n* __false\\_positive__ = the vulnerability is not specific to the component or service and was falsely identified or associated. \n* __not\\_affected__ = the component or service is not affected by the vulnerability. Justification should be specified for all not_affected cases.",
      "enum": [
        "resolved",
        "resolved_with_pedigree",
        "exploitable",
        "in_triage",
        "false_positive",
        "not_affected"
      ]
    },
    "impactAnalysisJustification": {
      "type": "string",
      "title": "Impact Analysis Justification",
      "description": "The rationale of why the impact analysis state was asserted. \n\n* __code\\_not\\_present__ = the code has been removed or tree-shaked. \n* __code\\_not\\_reachable__ = the vulnerable code is not invoked at runtime. \n* __requires\\_configuration__ = exploitability requires a configurable option to be set/unset. \n* __requires\\_dependency__ = exploitability requires a dependency that is not present. \n* __requires\\_environment__ = exploitability requires a certain environment which is not present. \n* __protected\\_by\\_compiler__ = exploitability requires a compiler flag to be set/unset. \n* __protected\\_at\\_runtime__ = exploits are prevented at runtime. \n* __protected\\_at\\_perimeter__ = attacks are blocked at physical, logical, or network perimeter. \n* __protected\\_by\\_mitigating\\_control__ = preventative measures have been implemented that reduce the likelihood and/or impact of the vulnerability.",
      "enum": [
        "code_not_present",
        "code_not_reachable",
        "requires_configuration",
        "requires_dependency",
        "requires_environment",
        "protected_by_compiler",
        "protected_at_runtime",
        "protected_at_perimeter",
        "protected_by_mitigating_control"
      ]
    },
    "rating": {
      "type": "object",
      "title": "Rating",
      "description": "Defines the severity or risk ratings of a vulnerability.",
      "additionalProperties": false,
      "properties": {
        "source": {
          "$ref": "#/definitions/vulnerabilitySource",
          "description": "The source that calculated the severity or risk rating of the vulnerability."
        },
        "score": {
          "type": "number",
          "title": "Score",
          "description": "The numerical score of the rating."
        },
        "severity": {
          "$ref": "#/definitions/severity",
          "description": "Textual representation of the severity that corresponds to the numerical score of the rating."
        },
        "method": {
          "$ref": "#/definitions/scoreMethod"
        },
        "vector": {
          "type": "string",
          "title": "Vector",
          "description": "Textual representation of the metric values used to score the vulnerability"
        },
        "justification": {
          "type": "string",
          "title": "Justification",
          "description": "An optional reason for rating the vulnerability as it was"
        }
      }
    },
    "vulnerabilitySource": {
      "type": "object",
      "title": "Source",
      "description": "The source of vulnerability information. This is often the organization that published the vulnerability.",
      "additionalProperties": false,
      "properties": {
        "url": {
          "type": "string",
          "title": "URL",
          "description": "The url of the vulnerability documentation as provided by the source.",
          "examples": [
            "https://nvd.nist.gov/vuln/detail/CVE-2021-39182"
          ]
        },
        "name": {
          "type": "string",
          "title": "Name",
          "description": "The name of the source.",
          "examples": [
            "NVD",
            "National Vulnerability Database",
            "OSS Index",
            "VulnDB",
            "GitHub Advisories"
          ]
        }
      }
    },
    "vulnerability": {
      "type": "object",
      "title": "Vulnerability",
      "description": "Defines a weakness in a component or service that could be exploited or triggered by a threat source.",
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "$ref": "#/definitions/refType",
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the vulnerability elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
        },
        "id": {
          "type": "string",
          "title": "ID",
          "description": "The identifier that uniquely identifies the vulnerability.",
          "examples": [
            "CVE-2021-39182",
            "GHSA-35m5-8cvj-8783",
            "SNYK-PYTHON-ENROCRYPT-1912876"
          ]
        },
        "source": {
          "$ref": "#/definitions/vulnerabilitySource",
          "description": "The source that published the vulnerability."
        },
        "references": {
          "type": "array",
          "title": "References",
          "description": "Zero or more pointers to vulnerabilities that are the equivalent of the vulnerability specified. Often times, the same vulnerability may exist in multiple sources of vulnerability intelligence, but have different identifiers. References provide a way to correlate vulnerabilities across multiple sources of vulnerability intelligence.",
          "items": {
            "type": "object",
            "required": [
              "id",
              "source"
            ],
            "additionalProperties": false,
            "properties": {
              "id": {
                "type": "string",
                "title": "ID",
                "description": "An identifier that uniquely identifies the vulnerability.",
                "examples": [
                  "CVE-2021-39182",
                  "GHSA-35m5-8cvj-8783",
                  "SNYK-PYTHON-ENROCRYPT-1912876"
                ]
              },
              "source": {
                "$ref": "#/definitions/vulnerabilitySource",
                "description": "The source that published the vulnerability."
              }
            }
          }
        },
        "ratings": {
          "type": "array",
          "title": "Ratings",
          "description": "List of vulnerability ratings",
          "items": {
            "$ref": "#/definitions/rating"
          }
        },
        "cwes": {
          "type": "array",
          "title": "CWEs",
          "description": "List of Common Weaknesses Enumerations (CWEs) codes that describes this vulnerability. For example 399 (of https://cwe.mitre.org/data/definitions/399.html)",
          "examples": [399],
          "items": {
            "$ref": "#/definitions/cwe"
          }
        },
        "description": {
          "type": "string",
          "title": "Description",
          "description": "A description of the vulnerability as provided by the source."
        },
        "detail": {
          "type": "string",
          "title": "Details",
          "description": "If available, an in-depth description of the vulnerability as provided by the source organization. Details often include information useful in understanding root cause."
        },
        "recommendation": {
          "type": "string",
          "title": "Recommendation",
          "description": "Recommendations of how the vulnerability can be remediated or mitigated."
        },
        "workaround": {
          "type": "string",
          "title": "Workarounds",
          "description": "A bypass, usually temporary, of the vulnerability that reduces its likelihood and/or impact. Workarounds often involve changes to configuration or deployments."
        },
        "proofOfConcept": {
          "type": "object",
          "title": "Proof of Concept",
          "description": "Evidence used to reproduce the vulnerability.",
          "properties": {
            "reproductionSteps": {
              "type": "string",
              "title": "Steps to Reproduce",
              "description": "Precise steps to reproduce the vulnerability."
            },
            "environment": {
              "type": "string",
              "title": "Environment",
              "description": "A description of the environment in which reproduction was possible."
            },
            "supportingMaterial": {
              "type": "array",
              "title": "Supporting Material",
              "description": "Supporting material that helps in reproducing or understanding how reproduction is possible. This may include screenshots, payloads, and PoC exploit code.",
              "items": { "$ref": "#/definitions/attachment" }
            }
          }
        },
        "advisories": {
          "type": "array",
          "title": "Advisories",
          "description": "Published advisories of the vulnerability if provided.",
          "items": {
            "$ref": "#/definitions/advisory"
          }
        },
        "created": {
          "type": "string",
          "format": "date-time",
          "title": "Created",
          "description": "The date and time (timestamp) when the vulnerability record was created in the vulnerability database."
        },
        "published": {
          "type": "string",
          "format": "date-time",
          "title": "Published",
          "description": "The date and time (timestamp) when the vulnerability record was first published."
        },
        "updated": {
          "type": "string",
          "format": "date-time",
          "title": "Updated",
          "description": "The date and time (timestamp) when the vulnerability record was last updated."
        },
        "rejected": {
          "type": "string",
          "format": "date-time",
          "title": "Rejected",
          "description": "The date and time (timestamp) when the vulnerability record was rejected (if applicable)."
        },
        "credits": {
          "type": "object",
          "title": "Credits",
          "description": "Individuals or organizations credited with the discovery of the vulnerability.",
          "additionalProperties": false,
          "properties": {
            "organizations": {
              "type": "array",
              "title": "Organizations",
              "description": "The organizations credited with vulnerability discovery.",
              "items": {
                "$ref": "#/definitions/organizationalEntity"
              }
            },
            "individuals": {
              "type": "array",
              "title": "Individuals",
              "description": "The individuals, not associated with organizations, that are credited with vulnerability discovery.",
              "items": {
                "$ref": "#/definitions/organizationalContact"
              }
            }
          }
        },
        "tools": {
          "oneOf": [
            {
              "type": "object",
              "title": "Tools",
              "description": "The tool(s) used to identify, confirm, or score the vulnerability.",
              "additionalProperties": false,
              "properties": {
                "components": {
                  "type": "array",
                  "items": {"$ref": "#/definitions/component"},
                  "uniqueItems": true,
                  "title": "Components",
                  "description": "A list of software and hardware components used as tools"
                },
                "services": {
                  "type": "array",
                  "items": {"$ref": "#/definitions/service"},
                  "uniqueItems": true,
                  "title": "Services",
                  "description": "A list of services used as tools. This may include microservices, function-as-a-service, and other types of network or intra-process services."
                }
              }
            },
            {
              "type": "array",
              "title": "Tools (legacy)",
              "description": "[Deprecated] The tool(s) used to identify, confirm, or score the vulnerability.",
              "items": {"$ref": "#/definitions/tool"}
            }
          ]
        },
        "analysis": {
          "type": "object",
          "title": "Impact Analysis",
          "description": "An assessment of the impact and exploitability of the vulnerability.",
          "additionalProperties": false,
          "properties": {
            "state": {
              "$ref": "#/definitions/impactAnalysisState"
            },
            "justification": {
              "$ref": "#/definitions/impactAnalysisJustification"
            },
            "response": {
              "type": "array",
              "title": "Response",
              "description": "A response to the vulnerability by the manufacturer, supplier, or project responsible for the affected component or service. More than one response is allowed. Responses are strongly encouraged for vulnerabilities where the analysis state is exploitable.",
              "items": {
                "type": "string",
                "enum": [
                  "can_not_fix",
                  "will_not_fix",
                  "update",
                  "rollback",
                  "workaround_available"
                ]
              }
            },
            "detail": {
              "type": "string",
              "title": "Detail",
              "description": "Detailed description of the impact including methods used during assessment. If a vulnerability is not exploitable, this field should include specific details on why the component or service is not impacted by this vulnerability."
            },
            "firstIssued": {
              "type": "string",
              "format": "date-time",
              "title": "First Issued",
              "description": "The date and time (timestamp) when the analysis was first issued."
            },
            "lastUpdated": {
              "type": "string",
              "format": "date-time",
              "title": "Last Updated",
              "description": "The date and time (timestamp) when the analysis was last updated."
            }
          }
        },
        "affects": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "type": "object",
            "required": [
              "ref"
            ],
            "additionalProperties": false,
            "properties": {
              "ref": {
                "anyOf": [
                  {
                    "title": "Ref",
                    "$ref": "#/definitions/refLinkType"
                  },
                  {
                    "title": "BOM-Link Element",
                    "$ref": "#/definitions/bomLinkElementType"
                  }
                ],
                "title": "Reference",
                "description": "References a component or service by the objects bom-ref"
              },
              "versions": {
                "type": "array",
                "title": "Versions",
                "description": "Zero or more individual versions or range of versions.",
                "items": {
                  "type": "object",
                  "oneOf": [
                    {
                      "required": ["version"]
                    },
                    {
                      "required": ["range"]
                    }
                  ],
                  "additionalProperties": false,
                  "properties": {
                    "version": {
                      "description": "A single version of a component or service.",
                      "$ref": "#/definitions/version"
                    },
                    "range": {
                      "description": "A version range specified in Package URL Version Range syntax (vers) which is defined at https://github.com/package-url/purl-spec/VERSION-RANGE-SPEC.rst",
                      "$ref": "#/definitions/range"
                    },
                    "status": {
                      "description": "The vulnerability status for the version or range of versions.",
                      "$ref": "#/definitions/affectedStatus",
                      "default": "affected"
                    }
                  }
                }
              }
            }
          },
          "title": "Affects",
          "description": "The components or services that are affected by the vulnerability."
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "description": "Provides the ability to document properties in a name-value store. This provides flexibility to include data not officially supported in the standard without having to use additional namespaces or create extensions. Unlike key-value stores, properties support duplicate names, each potentially having different values. Property names of interest to the general public are encouraged to be registered in the [CycloneDX Property Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy). Formal registration is OPTIONAL.",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "affectedStatus": {
      "description": "The vulnerability status of a given version or range of versions of a product. The statuses 'affected' and 'unaffected' indicate that the version is affected or unaffected by the vulnerability. The status 'unknown' indicates that it is unknown or unspecified whether the given version is affected. There can be many reasons for an 'unknown' status, including that an investigation has not been undertaken or that a vendor has not disclosed the status.",
      "type": "string",
      "enum": [
        "affected",
        "unaffected",
        "unknown"
      ]
    },
    "version": {
      "description": "A single version of a component or service.",
      "type": "string",
      "minLength": 1,
      "maxLength": 1024
    },
    "range": {
      "description": "A version range specified in Package URL Version Range syntax (vers) which is defined at https://github.com/package-url/purl-spec/VERSION-RANGE-SPEC.rst",
      "type": "string",
      "minLength": 1,
      "maxLength": 1024
    },
    "annotations": {
      "type": "object",
      "title": "Annotations",
      "description": "A comment, note, explanation, or similar textual content which provides additional context to the object(s) being annotated.",
      "required": [
        "subjects",
        "annotator",
        "timestamp",
        "text"
      ],
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "$ref": "#/definitions/refType",
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the annotation elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
        },
        "subjects": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "anyOf": [
              {
                "title": "Ref",
                "$ref": "#/definitions/refLinkType"
              },
              {
                "title": "BOM-Link Element",
                "$ref": "#/definitions/bomLinkElementType"
              }
            ]
          },
          "title": "BOM References",
          "description": "The object in the BOM identified by its bom-ref. This is often a component or service, but may be any object type supporting bom-refs."
        },
        "annotator": {
          "type": "object",
          "title": "Annotator",
          "description": "The organization, person, component, or service which created the textual content of the annotation.",
          "oneOf": [
            {
              "required": [
                "organization"
              ]
            },
            {
              "required": [
                "individual"
              ]
            },
            {
              "required": [
                "component"
              ]
            },
            {
              "required": [
                "service"
              ]
            }
          ],
          "additionalProperties": false,
          "properties": {
            "organization": {
              "description": "The organization that created the annotation",
              "$ref": "#/definitions/organizationalEntity"
            },
            "individual": {
              "description": "The person that created the annotation",
              "$ref": "#/definitions/organizationalContact"
            },
            "component": {
              "description": "The tool or component that created the annotation",
              "$ref": "#/definitions/component"
            },
            "service": {
              "description": "The service that created the annotation",
              "$ref": "#/definitions/service"
            }
          }
        },
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "title": "Timestamp",
          "description": "The date and time (timestamp) when the annotation was created."
        },
        "text": {
          "type": "string",
          "title": "Text",
          "description": "The textual content of the annotation."
        },
        "signature": {
          "$ref": "#/definitions/signature",
          "title": "Signature",
          "description": "Enveloped signature in [JSON Signature Format (JSF)](https://cyberphone.github.io/doc/security/jsf.html)."
        }
      }
    },
    "modelCard": {
      "$comment": "Model card support in CycloneDX is derived from TensorFlow Model Card Toolkit released under the Apache 2.0 license and available from https://github.com/tensorflow/model-card-toolkit/blob/main/model_card_toolkit/schema/v0.0.2/model_card.schema.json. In addition, CycloneDX model card support includes portions of VerifyML, also released under the Apache 2.0 license and available from https://github.com/cylynx/verifyml/blob/main/verifyml/model_card_toolkit/schema/v0.0.4/model_card.schema.json.",
      "type": "object",
      "title": "Model Card",
      "description": "A model card describes the intended uses of a machine learning model and potential limitations, including biases and ethical considerations. Model cards typically contain the training parameters, which datasets were used to train the model, performance metrics, and other relevant data useful for ML transparency. This object SHOULD be specified for any component of type `machine-learning-model` and MUST NOT be specified for other component types.",
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "$ref": "#/definitions/refType",
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the model card elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
        },
        "modelParameters": {
          "type": "object",
          "title": "Model Parameters",
          "description": "Hyper-parameters for construction of the model.",
          "additionalProperties": false,
          "properties": {
            "approach": {
              "type": "object",
              "title": "Approach",
              "description": "The overall approach to learning used by the model for problem solving.",
              "additionalProperties": false,
              "properties": {
                "type": {
                  "type": "string",
                  "title": "Learning Type",
                  "description": "Learning types describing the learning problem or hybrid learning problem.",
                  "enum": [
                    "supervised",
                    "unsupervised",
                    "reinforcement-learning",
                    "semi-supervised",
                    "self-supervised"
                  ]
                }
              }
            },
            "task": {
              "type": "string",
              "title": "Task",
              "description": "Directly influences the input and/or output. Examples include classification, regression, clustering, etc."
            },
            "architectureFamily": {
              "type": "string",
              "title": "Architecture Family",
              "description": "The model architecture family such as transformer network, convolutional neural network, residual neural network, LSTM neural network, etc."
            },
            "modelArchitecture": {
              "type": "string",
              "title": "Model Architecture",
              "description": "The specific architecture of the model such as GPT-1, ResNet-50, YOLOv3, etc."
            },
            "datasets": {
              "type": "array",
              "title": "Datasets",
              "description": "The datasets used to train and evaluate the model.",
              "items" : {
                "oneOf" : [
                  {
                    "title": "Inline Component Data",
                    "$ref": "#/definitions/componentData"
                  },
                  {
                    "type": "object",
                    "title": "Data Component Reference",
                    "additionalProperties": false,
                    "properties": {
                      "ref": {
                        "anyOf": [
                          {
                            "title": "Ref",
                            "$ref": "#/definitions/refLinkType"
                          },
                          {
                            "title": "BOM-Link Element",
                            "$ref": "#/definitions/bomLinkElementType"
                          }
                        ],
                        "title": "Reference",
                        "description": "References a data component by the components bom-ref attribute"
                      }
                    }
                  }
                ]
              }
            },
            "inputs": {
              "type": "array",
              "title": "Inputs",
              "description": "The input format(s) of the model",
              "items": { "$ref": "#/definitions/inputOutputMLParameters" }
            },
            "outputs": {
              "type": "array",
              "title": "Outputs",
              "description": "The output format(s) from the model",
              "items": { "$ref": "#/definitions/inputOutputMLParameters" }
            }
          }
        },
        "quantitativeAnalysis": {
          "type": "object",
          "title": "Quantitative Analysis",
          "description": "A quantitative analysis of the model",
          "additionalProperties": false,
          "properties": {
            "performanceMetrics": {
              "type": "array",
              "title": "Performance Metrics",
              "description": "The model performance metrics being reported. Examples may include accuracy, F1 score, precision, top-3 error rates, MSC, etc.",
              "items": { "$ref": "#/definitions/performanceMetric" }
            },
            "graphics": { "$ref": "#/definitions/graphicsCollection" }
          }
        },
        "considerations": {
          "type": "object",
          "title": "Considerations",
          "description": "What considerations should be taken into account regarding the model's construction, training, and application?",
          "additionalProperties": false,
          "properties": {
            "users": {
              "type": "array",
              "title": "Users",
              "description": "Who are the intended users of the model?",
              "items": {
                "type": "string"
              }
            },
            "useCases": {
              "type": "array",
              "title": "Use Cases",
              "description": "What are the intended use cases of the model?",
              "items": {
                "type": "string"
              }
            },
            "technicalLimitations": {
              "type": "array",
              "title": "Technical Limitations",
              "description": "What are the known technical limitations of the model? E.g. What kind(s) of data should the model be expected not to perform well on? What are the factors that might degrade model performance?",
              "items": {
                "type": "string"
              }
            },
            "performanceTradeoffs": {
              "type": "array",
              "title": "Performance Tradeoffs",
              "description": "What are the known tradeoffs in accuracy/performance of the model?",
              "items": {
                "type": "string"
              }
            },
            "ethicalConsiderations": {
              "type": "array",
              "title": "Ethical Considerations",
              "description": "What are the ethical (or environmental) risks involved in the application of this model?",
              "items": { "$ref": "#/definitions/risk" }
            },
            "fairnessAssessments": {
              "type": "array",
              "title": "Fairness Assessments",
              "description": "How does the model affect groups at risk of being systematically disadvantaged? What are the harms and benefits to the various affected groups?",
              "items": {
                "$ref": "#/definitions/fairnessAssessment"
              }
            }
          }
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "description": "Provides the ability to document properties in a name-value store. This provides flexibility to include data not officially supported in the standard without having to use additional namespaces or create extensions. Unlike key-value stores, properties support duplicate names, each potentially having different values. Property names of interest to the general public are encouraged to be registered in the [CycloneDX Property Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy). Formal registration is OPTIONAL.",
          "items": {"$ref": "#/definitions/property"}
        }
      }
    },
    "inputOutputMLParameters": {
      "type": "object",
      "title": "Input and Output Parameters",
      "additionalProperties": false,
      "properties": {
        "format": {
          "description": "The data format for input/output to the model. Example formats include string, image, time-series",
          "type": "string"
        }
      }
    },
    "componentData": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "type"
      ],
      "properties": {
        "bom-ref": {
          "$ref": "#/definitions/refType",
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the dataset elsewhere in the BOM. Every bom-ref MUST be unique within the BOM."
        },
        "type": {
          "type": "string",
          "title": "Type of Data",
          "description": "The general theme or subject matter of the data being specified.\n\n* __source-code__ = Any type of code, code snippet, or data-as-code.\n* __configuration__ = Parameters or settings that may be used by other components.\n* __dataset__ = A collection of data.\n* __definition__ = Data that can be used to create new instances of what the definition defines.\n* __other__ = Any other type of data that does not fit into existing definitions.",
          "enum": [
            "source-code",
            "configuration",
            "dataset",
            "definition",
            "other"
          ]
        },
        "name": {
          "description": "The name of the dataset.",
          "type": "string"
        },
        "contents": {
          "type": "object",
          "title": "Data Contents",
          "description": "The contents or references to the contents of the data being described.",
          "additionalProperties": false,
          "properties": {
            "attachment": {
              "title": "Data Attachment",
              "description": "An optional way to include textual or encoded data.",
              "$ref": "#/definitions/attachment"
            },
            "url": {
              "type": "string",
              "title": "Data URL",
              "description": "The URL to where the data can be retrieved.",
              "format": "iri-reference"
            },
            "properties": {
              "type": "array",
              "title": "Configuration Properties",
              "description": "Provides the ability to document name-value parameters used for configuration.",
              "items": {
                "$ref": "#/definitions/property"
              }
            }
          }
        },
        "classification": {
          "$ref": "#/definitions/dataClassification"
        },
        "sensitiveData": {
          "type": "array",
          "description": "A description of any sensitive data in a dataset.",
          "items": {
            "type": "string"
          }
        },
        "graphics": { "$ref": "#/definitions/graphicsCollection" },
        "description": {
          "description": "A description of the dataset. Can describe size of dataset, whether it's used for source code, training, testing, or validation, etc.",
          "type": "string"
        },
        "governance": {
          "type": "object",
          "title": "Data Governance",
          "$ref": "#/definitions/dataGovernance"
        }
      }
    },
    "dataGovernance": {
      "type": "object",
      "title": "Data Governance",
      "additionalProperties": false,
      "properties": {
        "custodians": {
          "type": "array",
          "title": "Data Custodians",
          "description": "Data custodians are responsible for the safe custody, transport, and storage of data.",
          "items": { "$ref": "#/definitions/dataGovernanceResponsibleParty" }
        },
        "stewards": {
          "type": "array",
          "title": "Data Stewards",
          "description": "Data stewards are responsible for data content, context, and associated business rules.",
          "items": { "$ref": "#/definitions/dataGovernanceResponsibleParty" }
        },
        "owners": {
          "type": "array",
          "title": "Data Owners",
          "description": "Data owners are concerned with risk and appropriate access to data.",
          "items": { "$ref": "#/definitions/dataGovernanceResponsibleParty" }
        }
      }
    },
    "dataGovernanceResponsibleParty": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "organization": {
          "title": "Organization",
          "$ref": "#/definitions/organizationalEntity"
        },
        "contact": {
          "title": "Individual",
          "$ref": "#/definitions/organizationalContact"
        }
      },
      "oneOf":[
        {
          "required": ["organization"]
        },
        {
          "required": ["contact"]
        }
      ]
    },
    "graphicsCollection": {
      "type": "object",
      "title": "Graphics Collection",
      "description": "A collection of graphics that represent various measurements.",
      "additionalProperties": false,
      "properties": {
        "description": {
          "description": "A description of this collection of graphics.",
          "type": "string"
        },
        "collection": {
          "description": "A collection of graphics.",
          "type": "array",
          "items": { "$ref": "#/definitions/graphic" }
        }
      }
    },
    "graphic": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "name": {
          "description": "The name of the graphic.",
          "type": "string"
        },
        "image": {
          "title": "Graphic Image",
          "description": "The graphic (vector or raster). Base64 encoding MUST be specified for binary images.",
          "$ref": "#/definitions/attachment"
        }
      }
    },
    "performanceMetric": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "type": {
          "description": "The type of performance metric.",
          "type": "string"
        },
        "value": {
          "description": "The value of the performance metric.",
          "type": "string"
        },
        "slice": {
          "description": "The name of the slice this metric was computed on. By default, assume this metric is not sliced.",
          "type": "string"
        },
        "confidenceInterval": {
          "description": "The confidence interval of the metric.",
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "lowerBound": {
              "description": "The lower bound of the confidence interval.",
              "type": "string"
            },
            "upperBound": {
              "description": "The upper bound of the confidence interval.",
              "type": "string"
            }
          }
        }
      }
    },
    "risk": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "name": {
          "description": "The name of the risk.",
          "type": "string"
        },
        "mitigationStrategy": {
          "description": "Strategy used to address this risk.",
          "type": "string"
        }
      }
    },
    "fairnessAssessment": {
      "type": "object",
      "title": "Fairness Assessment",
      "description": "Information about the benefits and harms of the model to an identified at risk group.",
      "additionalProperties": false,
      "properties": {
        "groupAtRisk": {
          "type": "string",
          "description": "The groups or individuals at risk of being systematically disadvantaged by the model."
        },
        "benefits": {
          "type": "string",
          "description": "Expected benefits to the identified groups."
        },
        "harms": {
          "type": "string",
          "description": "Expected harms to the identified groups."
        },
        "mitigationStrategy": {
          "type": "string",
          "description": "With respect to the benefits and harms outlined, please describe any mitigation strategy implemented."
        }
      }
    },
    "dataClassification": {
      "type": "string",
      "title": "Data Classification",
      "description": "Data classification tags data according to its type, sensitivity, and value if altered, stolen, or destroyed."
    },
    "formula": {
      "title": "Formula",
      "description": "Describes workflows and resources that captures rules and other aspects of how the associated BOM component or service was formed.",
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the formula elsewhere in the BOM. Every bom-ref MUST be unique within the BOM.",
          "$ref": "#/definitions/refType"
        },
        "components": {
          "title": "Components",
          "description": "Transient components that are used in tasks that constitute one or more of this formula's workflows",
          "type": "array",
          "items": {
            "$ref": "#/definitions/component"
          },
          "uniqueItems": true
        },
        "services": {
          "title": "Services",
          "description": "Transient services that are used in tasks that constitute one or more of this formula's workflows",
          "type": "array",
          "items": {
            "$ref": "#/definitions/service"
          },
          "uniqueItems": true
        },
        "workflows": {
          "title": "Workflows",
          "description": "List of workflows that can be declared to accomplish specific orchestrated goals and independently triggered.",
          "$comment": "Different workflows can be designed to work together to perform end-to-end CI/CD builds and deployments.",
          "type": "array",
          "items": {
            "$ref": "#/definitions/workflow"
          },
          "uniqueItems": true
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "workflow": {
      "title": "Workflow",
      "description": "A specialized orchestration task.",
      "$comment": "Workflow are as task themselves and can trigger other workflow tasks.  These relationships can be modeled in the taskDependencies graph.",
      "type": "object",
      "required": [
        "bom-ref",
        "uid",
        "taskTypes"
      ],
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the workflow elsewhere in the BOM. Every bom-ref MUST be unique within the BOM.",
          "$ref": "#/definitions/refType"
        },
        "uid": {
          "title": "Unique Identifier (UID)",
          "description": "The unique identifier for the resource instance within its deployment context.",
          "type": "string"
        },
        "name": {
          "title": "Name",
          "description": "The name of the resource instance.",
          "type": "string"
        },
        "description": {
          "title": "Description",
          "description": "A description of the resource instance.",
          "type": "string"
        },
        "resourceReferences": {
          "title": "Resource references",
          "description": "References to component or service resources that are used to realize the resource instance.",
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/resourceReferenceChoice"
          }
        },
        "tasks": {
          "title": "Tasks",
          "description": "The tasks that comprise the workflow.",
          "$comment": "Note that tasks can appear more than once as different instances (by name or UID).",
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/task"
          }
        },
        "taskDependencies": {
          "title": "Task dependency graph",
          "description": "The graph of dependencies between tasks within the workflow.",
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/dependency"
          }
        },
        "taskTypes": {
          "title": "Task types",
          "description": "Indicates the types of activities performed by the set of workflow tasks.",
          "$comment": "Currently, these types reflect common CI/CD actions.",
          "type": "array",
          "items": {
            "$ref": "#/definitions/taskType"
          }
        },
        "trigger": {
          "title": "Trigger",
          "description": "The trigger that initiated the task.",
          "$ref": "#/definitions/trigger"
        },
        "steps": {
          "title": "Steps",
          "description": "The sequence of steps for the task.",
          "type": "array",
          "items": {
            "$ref": "#/definitions/step"
          },
          "uniqueItems": true
        },
        "inputs": {
          "title": "Inputs",
          "description": "Represents resources and data brought into a task at runtime by executor or task commands",
          "examples": ["a `configuration` file which was declared as a local `component` or `externalReference`"],
          "type": "array",
          "items": {
            "$ref": "#/definitions/inputType"
          },
          "uniqueItems": true
        },
        "outputs": {
          "title": "Outputs",
          "description": "Represents resources and data output from a task at runtime by executor or task commands",
          "examples": ["a log file or metrics data produced by the task"],
          "type": "array",
          "items": {
            "$ref": "#/definitions/outputType"
          },
          "uniqueItems": true
        },
        "timeStart": {
          "title": "Time start",
          "description": "The date and time (timestamp) when the task started.",
          "type": "string",
          "format": "date-time"
        },
        "timeEnd": {
          "title": "Time end",
          "description": "The date and time (timestamp) when the task ended.",
          "type": "string",
          "format": "date-time"
        },
        "workspaces": {
          "title": "Workspaces",
          "description": "A set of named filesystem or data resource shareable by workflow tasks.",
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/workspace"
          }
        },
        "runtimeTopology": {
          "title": "Runtime topology",
          "description": "A graph of the component runtime topology for workflow's instance.",
          "$comment": "A description of the runtime component and service topology.  This can describe a partial or complete topology used to host and execute the task (e.g., hardware, operating systems, configurations, etc.),",
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/dependency"
          }
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "task": {
      "title": "Task",
      "description": "Describes the inputs, sequence of steps and resources used to accomplish a task and its output.",
      "$comment": "Tasks are building blocks for constructing assemble CI/CD workflows or pipelines.",
      "type": "object",
      "required": [
        "bom-ref",
        "uid",
        "taskTypes"
      ],
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the task elsewhere in the BOM. Every bom-ref MUST be unique within the BOM.",
          "$ref": "#/definitions/refType"
        },
        "uid": {
          "title": "Unique Identifier (UID)",
          "description": "The unique identifier for the resource instance within its deployment context.",
          "type": "string"
        },
        "name": {
          "title": "Name",
          "description": "The name of the resource instance.",
          "type": "string"
        },
        "description": {
          "title": "Description",
          "description": "A description of the resource instance.",
          "type": "string"
        },
        "resourceReferences": {
          "title": "Resource references",
          "description": "References to component or service resources that are used to realize the resource instance.",
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/resourceReferenceChoice"
          }
        },
        "taskTypes": {
          "title": "Task types",
          "description": "Indicates the types of activities performed by the set of workflow tasks.",
          "$comment": "Currently, these types reflect common CI/CD actions.",
          "type": "array",
          "items": {
            "$ref": "#/definitions/taskType"
          }
        },
        "trigger": {
          "title": "Trigger",
          "description": "The trigger that initiated the task.",
          "$ref": "#/definitions/trigger"
        },
        "steps": {
          "title": "Steps",
          "description": "The sequence of steps for the task.",
          "type": "array",
          "items": {
            "$ref": "#/definitions/step"
          },
          "uniqueItems": true
        },
        "inputs": {
          "title": "Inputs",
          "description": "Represents resources and data brought into a task at runtime by executor or task commands",
          "examples": ["a `configuration` file which was declared as a local `component` or `externalReference`"],
          "type": "array",
          "items": {
            "$ref": "#/definitions/inputType"
          },
          "uniqueItems": true
        },
        "outputs": {
          "title": "Outputs",
          "description": "Represents resources and data output from a task at runtime by executor or task commands",
          "examples": ["a log file or metrics data produced by the task"],
          "type": "array",
          "items": {
            "$ref": "#/definitions/outputType"
          },
          "uniqueItems": true
        },
        "timeStart": {
          "title": "Time start",
          "description": "The date and time (timestamp) when the task started.",
          "type": "string",
          "format": "date-time"
        },
        "timeEnd": {
          "title": "Time end",
          "description": "The date and time (timestamp) when the task ended.",
          "type": "string",
          "format": "date-time"
        },
        "workspaces": {
          "title": "Workspaces",
          "description": "A set of named filesystem or data resource shareable by workflow tasks.",
          "type": "array",
          "items": {
            "$ref": "#/definitions/workspace"
          },
          "uniqueItems": true
        },
        "runtimeTopology": {
          "title": "Runtime topology",
          "description": "A graph of the component runtime topology for task's instance.",
          "$comment": "A description of the runtime component and service topology.  This can describe a partial or complete topology used to host and execute the task (e.g., hardware, operating systems, configurations, etc.),",
          "type": "array",
          "items": {
            "$ref": "#/definitions/dependency"
          },
          "uniqueItems": true
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "step": {
      "type": "object",
      "description": "Executes specific commands or tools in order to accomplish its owning task as part of a sequence.",
      "additionalProperties": false,
      "properties": {
        "name": {
          "title": "Name",
          "description": "A name for the step.",
          "type": "string"
        },
        "description": {
          "title": "Description",
          "description": "A description of the step.",
          "type": "string"
        },
        "commands": {
          "title": "Commands",
          "description": "Ordered list of commands or directives for the step",
          "type": "array",
          "items": {
            "$ref": "#/definitions/command"
          }
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "command": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "executed": {
          "title": "Executed",
          "description": "A text representation of the executed command.",
          "type": "string"
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "workspace": {
      "title": "Workspace",
      "description": "A named filesystem or data resource shareable by workflow tasks.",
      "type": "object",
      "required": [
        "bom-ref",
        "uid"
      ],
      "additionalProperties": false,
      "properties": {
        "bom-ref": {
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the workspace elsewhere in the BOM. Every bom-ref MUST be unique within the BOM.",
          "$ref": "#/definitions/refType"
        },
        "uid": {
          "title": "Unique Identifier (UID)",
          "description": "The unique identifier for the resource instance within its deployment context.",
          "type": "string"
        },
        "name": {
          "title": "Name",
          "description": "The name of the resource instance.",
          "type": "string"
        },
        "aliases": {
          "title": "Aliases",
          "description": "The names for the workspace as referenced by other workflow tasks. Effectively, a name mapping so other tasks can use their own local name in their steps.",
          "type": "array",
          "items": {"type": "string"}
        },
        "description": {
          "title": "Description",
          "description": "A description of the resource instance.",
          "type": "string"
        },
        "resourceReferences": {
          "title": "Resource references",
          "description": "References to component or service resources that are used to realize the resource instance.",
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/resourceReferenceChoice"
          }
        },
        "accessMode": {
          "title": "Access mode",
          "description": "Describes the read-write access control for the workspace relative to the owning resource instance.",
          "type": "string",
          "enum": [
            "read-only",
            "read-write",
            "read-write-once",
            "write-once",
            "write-only"
          ]
        },
        "mountPath": {
          "title": "Mount path",
          "description": "A path to a location on disk where the workspace will be available to the associated task's steps.",
          "type": "string"
        },
        "managedDataType": {
          "title": "Managed data type",
          "description": "The name of a domain-specific data type the workspace represents.",
          "$comment": "This property is for CI/CD frameworks that are able to provide access to structured, managed data at a more granular level than a filesystem.",
          "examples": ["ConfigMap","Secret"],
          "type": "string"
        },
        "volumeRequest": {
          "title": "Volume request",
          "description": "Identifies the reference to the request for a specific volume type and parameters.",
          "examples": ["a kubernetes Persistent Volume Claim (PVC) name"],
          "type": "string"
        },
        "volume": {
          "title": "Volume",
          "description": "Information about the actual volume instance allocated to the workspace.",
          "$comment": "The actual volume allocated may be different than the request.",
          "examples": ["see https://kubernetes.io/docs/concepts/storage/persistent-volumes/"],
          "$ref": "#/definitions/volume"
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "volume": {
      "title": "Volume",
      "description": "An identifiable, logical unit of data storage tied to a physical device.",
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "uid": {
          "title": "Unique Identifier (UID)",
          "description": "The unique identifier for the volume instance within its deployment context.",
          "type": "string"
        },
        "name": {
          "title": "Name",
          "description": "The name of the volume instance",
          "type": "string"
        },
        "mode": {
          "title": "Mode",
          "description": "The mode for the volume instance.",
          "type": "string",
          "enum": [
            "filesystem", "block"
          ],
          "default": "filesystem"
        },
        "path": {
          "title": "Path",
          "description": "The underlying path created from the actual volume.",
          "type": "string"
        },
        "sizeAllocated": {
          "title": "Size allocated",
          "description": "The allocated size of the volume accessible to the associated workspace. This should include the scalar size as well as IEC standard unit in either decimal or binary form.",
          "examples": ["10GB", "2Ti", "1Pi"],
          "type": "string"
        },
        "persistent": {
          "title": "Persistent",
          "description": "Indicates if the volume persists beyond the life of the resource it is associated with.",
          "type": "boolean"
        },
        "remote": {
          "title": "Remote",
          "description": "Indicates if the volume is remotely (i.e., network) attached.",
          "type": "boolean"
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "trigger": {
      "title": "Trigger",
      "description": "Represents a resource that can conditionally activate (or fire) tasks based upon associated events and their data.",
      "type": "object",
      "additionalProperties": false,
      "required": [
        "type",
        "bom-ref",
        "uid"
      ],
      "properties": {
        "bom-ref": {
          "title": "BOM Reference",
          "description": "An optional identifier which can be used to reference the trigger elsewhere in the BOM. Every bom-ref MUST be unique within the BOM.",
          "$ref": "#/definitions/refType"
        },
        "uid": {
          "title": "Unique Identifier (UID)",
          "description": "The unique identifier for the resource instance within its deployment context.",
          "type": "string"
        },
        "name": {
          "title": "Name",
          "description": "The name of the resource instance.",
          "type": "string"
        },
        "description": {
          "title": "Description",
          "description": "A description of the resource instance.",
          "type": "string"
        },
        "resourceReferences": {
          "title": "Resource references",
          "description": "References to component or service resources that are used to realize the resource instance.",
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/resourceReferenceChoice"
          }
        },
        "type": {
          "title": "Type",
          "description": "The source type of event which caused the trigger to fire.",
          "type": "string",
          "enum": [
            "manual",
            "api",
            "webhook",
            "scheduled"
          ]
        },
        "event": {
          "title": "Event",
          "description": "The event data that caused the associated trigger to activate.",
          "$ref": "#/definitions/event"
        },
        "conditions": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/condition"
          }
        },
        "timeActivated": {
          "title": "Time activated",
          "description": "The date and time (timestamp) when the trigger was activated.",
          "type": "string",
          "format": "date-time"
        },
        "inputs": {
          "title": "Inputs",
          "description": "Represents resources and data brought into a task at runtime by executor or task commands",
          "examples": ["a `configuration` file which was declared as a local `component` or `externalReference`"],
          "type": "array",
          "items": {
            "$ref": "#/definitions/inputType"
          },
          "uniqueItems": true
        },
        "outputs": {
          "title": "Outputs",
          "description": "Represents resources and data output from a task at runtime by executor or task commands",
          "examples": ["a log file or metrics data produced by the task"],
          "type": "array",
          "items": {
            "$ref": "#/definitions/outputType"
          },
          "uniqueItems": true
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "event": {
      "title": "Event",
      "description": "Represents something that happened that may trigger a response.",
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "uid": {
          "title": "Unique Identifier (UID)",
          "description": "The unique identifier of the event.",
          "type": "string"
        },
        "description": {
          "title": "Description",
          "description": "A description of the event.",
          "type": "string"
        },
        "timeReceived": {
          "title": "Time Received",
          "description": "The date and time (timestamp) when the event was received.",
          "type": "string",
          "format": "date-time"
        },
        "data": {
          "title": "Data",
          "description": "Encoding of the raw event data.",
          "$ref": "#/definitions/attachment"
        },
        "source": {
          "title": "Source",
          "description": "References the component or service that was the source of the event",
          "$ref": "#/definitions/resourceReferenceChoice"
        },
        "target": {
          "title": "Target",
          "description": "References the component or service that was the target of the event",
          "$ref": "#/definitions/resourceReferenceChoice"
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "inputType": {
      "title": "Input type",
      "description": "Type that represents various input data types and formats.",
      "type": "object",
      "oneOf": [
        {
          "required": [
            "resource"
          ]
        },
        {
          "required": [
            "parameters"
          ]
        },
        {
          "required": [
            "environmentVars"
          ]
        },
        {
          "required": [
            "data"
          ]
        }
      ],
      "additionalProperties": false,
      "properties": {
        "source": {
          "title": "Source",
          "description": "A references to the component or service that provided the input to the task (e.g., reference to a service with data flow value of `inbound`)",
          "examples": [
            "source code repository",
            "database"
          ],
          "$ref": "#/definitions/resourceReferenceChoice"
        },
        "target": {
          "title": "Target",
          "description": "A reference to the component or service that received or stored the input if not the task itself (e.g., a local, named storage workspace)",
          "examples": [
            "workspace",
            "directory"
          ],
          "$ref": "#/definitions/resourceReferenceChoice"
        },
        "resource": {
          "title": "Resource",
          "description": "A reference to an independent resource provided as an input to a task by the workflow runtime.",
          "examples": [
            "reference to a configuration file in a repository (i.e., a bom-ref)",
            "reference to a scanning service used in a task (i.e., a bom-ref)"
          ],
          "$ref": "#/definitions/resourceReferenceChoice"
        },
        "parameters": {
          "title": "Parameters",
          "description": "Inputs that have the form of parameters with names and values.",
          "type": "array",
          "uniqueItems": true,
          "items": {
            "$ref": "#/definitions/parameter"
          }
        },
        "environmentVars": {
          "title": "Environment variables",
          "description": "Inputs that have the form of parameters with names and values.",
          "type": "array",
          "uniqueItems": true,
          "items": {
            "oneOf": [
              {
                "$ref": "#/definitions/property"
              },
              {
                "type": "string"
              }
            ]
          }
        },
        "data": {
          "title": "Data",
          "description": "Inputs that have the form of data.",
          "$ref": "#/definitions/attachment"
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "outputType": {
      "type": "object",
      "oneOf": [
        {
          "required": [
            "resource"
          ]
        },
        {
          "required": [
            "environmentVars"
          ]
        },
        {
          "required": [
            "data"
          ]
        }
      ],
      "additionalProperties": false,
      "properties": {
        "type": {
          "title": "Type",
          "description": "Describes the type of data output.",
          "type": "string",
          "enum": [
            "artifact",
            "attestation",
            "log",
            "evidence",
            "metrics",
            "other"
          ]
        },
        "source": {
          "title": "Source",
          "description": "Component or service that generated or provided the output from the task (e.g., a build tool)",
          "$ref": "#/definitions/resourceReferenceChoice"
        },
        "target": {
          "title": "Target",
          "description": "Component or service that received the output from the task (e.g., reference to an artifactory service with data flow value of `outbound`)",
          "examples": ["a log file described as an `externalReference` within its target domain."],
          "$ref": "#/definitions/resourceReferenceChoice"
        },
        "resource": {
          "title": "Resource",
          "description": "A reference to an independent resource generated as output by the task.",
          "examples": [
            "configuration file",
            "source code",
            "scanning service"
          ],
          "$ref": "#/definitions/resourceReferenceChoice"
        },
        "data": {
          "title": "Data",
          "description": "Outputs that have the form of data.",
          "$ref": "#/definitions/attachment"
        },
        "environmentVars": {
          "title": "Environment variables",
          "description": "Outputs that have the form of environment variables.",
          "type": "array",
          "items": {
            "oneOf": [
              {
                "$ref": "#/definitions/property"
              },
              {
                "type": "string"
              }
            ]
          },
          "uniqueItems": true
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "resourceReferenceChoice": {
      "title": "Resource reference choice",
      "description": "A reference to a locally defined resource (e.g., a bom-ref) or an externally accessible resource.",
      "$comment": "Enables reference to a resource that participates in a workflow; using either internal (bom-ref) or external (externalReference) types.",
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "ref": {
          "title": "BOM Reference",
          "description": "References an object by its bom-ref attribute",
          "anyOf": [
            {
              "title": "Ref",
              "$ref": "#/definitions/refLinkType"
            },
            {
              "title": "BOM-Link Element",
              "$ref": "#/definitions/bomLinkElementType"
            }
          ]
        },
        "externalReference": {
          "title": "External reference",
          "description": "Reference to an externally accessible resource.",
          "$ref": "#/definitions/externalReference"
        }
      },
      "oneOf": [
        {
          "required": [
            "ref"
          ]
        },
        {
          "required": [
            "externalReference"
          ]
        }
      ]
    },
    "condition": {
      "title": "Condition",
      "description": "A condition that was used to determine a trigger should be activated.",
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "description": {
          "title": "Description",
          "description": "Describes the set of conditions which cause the trigger to activate.",
          "type": "string"
        },
        "expression": {
          "title": "Expression",
          "description": "The logical expression that was evaluated that determined the trigger should be fired.",
          "type": "string"
        },
        "properties": {
          "type": "array",
          "title": "Properties",
          "items": {
            "$ref": "#/definitions/property"
          }
        }
      }
    },
    "taskType": {
      "type": "string",
      "enum": [
        "copy",
        "clone",
        "lint",
        "scan",
        "merge",
        "build",
        "test",
        "deliver",
        "deploy",
        "release",
        "clean",
        "other"
      ]
    },
    "parameter": {
      "title": "Parameter",
      "description": "A representation of a functional parameter.",
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "name": {
          "title": "Name",
          "description": "The name of the parameter.",
          "type": "string"
        },
        "value": {
          "title": "Value",
          "description": "The value of the parameter.",
          "type": "string"
        },
        "dataType": {
          "title": "Data type",
          "description": "The data type of the parameter.",
          "type": "string"
        }
      }
    },
    "signature": {
      "$ref": "jsf-0.82.schema.json#/definitions/signature",
      "title": "Signature",
      "description": "Enveloped signature in [JSON Signature Format (JSF)](https://cyberphone.github.io/doc/security/jsf.html)."
    }
  }
}
```