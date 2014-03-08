#!/usr/bin/python

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

class SIXAnalyzer_rules():

    config = configparser.SafeConfigParser(
        {
            'extensions': "*.h,*.hh,*.hpp",
        })

    cfg_dir = './'
    cfg_file = 'rules.ini'
    cfg_full_path = cfg_dir + cfg_file

    namespace = 'DEFAULT'
    config.read(cfg_full_path)
    print("PATH: %s"% cfg_full_path)
    to_ignore = [ 
        "BASE_DECL_ALIGNED_MEMORY()",
        "BASE_EXPORT",
        "BEGIN_BLUETOOTH_NAMESPACE",
        "BEGIN_FILE_NAMESPACE",
        "BEGIN_FMRADIO_NAMESPACE",
        "BEGIN_INDEXEDDB_NAMESPACE",
        "BEGIN_QUOTA_NAMESPACE",
        "BEGIN_TELEPHONY_NAMESPACE",
        "BEGIN_WORKERS_NAMESPACE",
        "DECLARE_ALIGNED()",
        "DECLARE_NS_PTR()",
        "DECL_STYLE_RULE_INHERIT",
        "DECL_STYLE_RULE_INHERIT_NO_DOMRULE",
        "DEFINE_SIZE_ARRAY",
        "DEFINE_SIZE_STATIC()",
        "DEFINE_int32()",
        "GMOCK_DEFINE_DEFAULT_ACTION_FOR_RETURN_TYPE_()",
        "GOOGLE_GLOG_DLL_DECL",
        "GR_STATIC_ASSERT()",
        "GTEST_API_",
        "GTEST_LOCK_EXCLUDED_",
        "G_DEFINE_TYPE_EXTENDED()",
        "G_IMPLEMENT_INTERFACE()",
        "JS_FRIEND_API",
        "JS_STATIC_ASSERT()",
        "LIBPROTOBUF_EXPORT",
        "MOZ_ALIGNED_DECL()",
        "MOZ_BEGIN_ENUM_CLASS()",
        "MOZ_DEFINE_MALLOC_SIZE_OF()",
        "MOZ_END_ENUM_CLASS()",
        "MOZ_EXPORT",
        "MOZ_FINAL",
        "MOZ_NONHEAP_CLASS",
        "MOZ_STACK_CLASS",
        "MOZ_STATIC_ASSERT()",
        "NS_COM_GLUE",
        "NS_DECLARE_FRAME_PROPERTY()",
        "NS_DECLARE_STATIC_IID_ACCESSOR()",
        "NS_DECL_CYCLE_COLLECTING_ISUPPORTS",
        "NS_DECL_CYCLE_COLLECTION_CLASS()",
        "NS_DECL_CYCLE_COLLECTION_CLASS_AMBIGUOUS()",
        "NS_DECL_CYCLE_COLLECTION_CLASS_INHERITED()",
        "NS_DECL_CYCLE_COLLECTION_CLASS_INHERITED_NO_UNLINK()",
        "NS_DECL_CYCLE_COLLECTION_SCRIPT_HOLDER_CLASS_AMBIGUOUS()",
        "NS_DECL_FRAMEARENA_HELPERS",
        "NS_DECL_ISUPPORTS",
        "NS_DECL_ISUPPORTS_INHERITED",
        "NS_DECL_NSIDIRECTORYSERVICEPROVIDER",
        "NS_DECL_NSIDIRECTORYSERVICEPROVIDER2",
        "NS_DECL_NSIDNSLISTENER",
        "NS_DECL_NSIDOMDOCUMENT",
        "NS_DECL_NSIDOMDOCUMENTXBL",
        "NS_DECL_NSIDOMHTMLINPUTELEMENT",
        "NS_DECL_NSIDOMXMLDOCUMENT",
        "NS_DECL_NSILISTBOXOBJECT",
        "NS_DECL_NSIOBSERVER",
        "NS_DECL_NSIPHONETIC",
        "NS_DECL_NSIREQUEST",
        "NS_DECL_NSITIMERCALLBACK",
        "NS_DECL_NSIURLCLASSIFIERDBSERVICE",
        "NS_DECL_NSIURLCLASSIFIERDBSERVICEWORKER",
        "NS_DECL_NSIURLCLASSIFIERLOOKUPCALLBACK",
        "NS_DECL_QUERYFRAME",
        "NS_DECL_QUERYFRAME_TARGET()",
        "NS_DECL_THREADSAFE_ISUPPORTS",
        "NS_DEFINE_STATIC_IID_ACCESSOR()",
        "NS_DISPLAY_DECL_NAME()",
        "NS_FORWARD_NSIDOMELEMENT_TO_GENERIC",
        "NS_FORWARD_NSIDOMHTMLELEMENT_TO_GENERIC",
        "NS_FORWARD_NSIDOMNODE_TO_NSINODE",
        "NS_FORWARD_NSIDOMNODE_TO_NSINODE_OVERRIDABLE",
        "NS_GENERIC_FACTORY_SINGLETON_CONSTRUCTOR()",
        "NS_GFX",
        "NS_IMPL_ADDREF_INHERITED()",
        "NS_IMPL_CYCLE_COLLECTION_INHERITED_1()",
        "NS_IMPL_CYCLE_COLLECTION_INHERITED_2",
        "NS_IMPL_CYCLE_COLLECTION_INHERITED_3()",
        "NS_IMPL_CYCLE_COLLECTION_INHERITED_4()",
        "NS_IMPL_CYCLE_COLLECTION_INHERITED_5()",
        "NS_IMPL_CYCLE_COLLECTION_INHERITED_6()",
        "NS_IMPL_CYCLE_COLLECTION_ROOT_NATIVE()",
        "NS_IMPL_CYCLE_COLLECTION_TRACE_WRAPPERCACHE()",
        "NS_IMPL_CYCLE_COLLECTION_TRAVERSE()",
        "NS_IMPL_CYCLE_COLLECTION_TRAVERSE_BEGIN()",
        "NS_IMPL_CYCLE_COLLECTION_TRAVERSE_END",
        "NS_IMPL_CYCLE_COLLECTION_TRAVERSE_SCRIPT_OBJECTS",
        "NS_IMPL_CYCLE_COLLECTION_UNLINK()",
        "NS_IMPL_CYCLE_COLLECTION_UNLINK_END",
        "NS_IMPL_CYCLE_COLLECTION_UNLINK_PRESERVED_WRAPPER",
        "NS_IMPL_CYCLE_COLLECTION_UNROOT_NATIVE()",
        "NS_IMPL_CYCLE_COLLECTION_WRAPPERCACHE_1()",
        "NS_IMPL_FRAMEARENA_HELPERS()",
        "NS_IMPL_FROMCONTENT_HTML_WITH_TAG()",
        "NS_IMPL_ISUPPORTS0()",
        "NS_IMPL_ISUPPORTS1()",
        "NS_IMPL_ISUPPORTS2()",
        "NS_IMPL_ISUPPORTS_INHERITED0()",
        "NS_IMPL_ISUPPORTS_INHERITED1()",
        "NS_IMPL_ISUPPORTS_INHERITED2()"
        "NS_IMPL_RELEASE_INHERITED()",
        "NS_INTERFACE_MAP_BEGIN_CYCLE_COLLECTION_INHERITED()",
        "NS_INTERFACE_MAP_END_INHERITING()",
        "NS_INTERFACE_MAP_ENTRY()",
        "NS_INTERFACE_MAP_ENTRY_AMBIGUOUS()",
        "NS_MUST_OVERRIDE",
        "NS_NO_VTABLE",
        "NS_OFFLINESTORAGE_IID",
        "NS_QUERYFRAME_ENTRY()",
        "NS_QUERYFRAME_HEAD()",
        "NS_QUERYFRAME_TAIL_INHERITING()",
        "NS_STACK_CLASS",
        "PNG_EXPORT()",
        "PNG_EXPORTA()",
        "PNG_INTERNAL_DATA()",
        "PR_IMPLEMENT()",
        "PR_STATIC_ASSERT()",
        "SDT_PROBE_ARGTYPE()",
        "SK_API",
        "SK_DECLARE_FLATTENABLE_REGISTRAR_GROUP()",
        "SK_DECLARE_PUBLIC_FLATTENABLE_DESERIALIZATION_PROCS()",
        "SK_DEFINE_FLATTENABLE_TYPE()",
        "SK_DEVELOPER_TO_STRING()",
        "TRACE_EVENT_API_CLASS_EXPORT",
        "T_CTEST_EXPORT_API",
        "USING_BLUETOOTH_NAMESPACE",
        "U_CDECL_END",
        "U_COMMON_API",
        "U_I18N_API",
        "U_NAMESPACE_BEGIN",
        "U_TOOLUTIL_API",
        "WEBRTC_DLLEXPORT",
        "ZEXPORT",
        "ZEXTERN",
        "ZLIB_INTERNAL",
        "_MYCLASS_",
        "_STLP_BEGIN_NAMESPACE",
        "_STLP_CLASS_DECLSPEC",
        "_STLP_DECLSPEC",
        "_STLP_MOVE_TO_PRIV_NAMESPACE",
        "_STLP_MOVE_TO_STD_NAMESPACE",
        "_STLP_NOTHROW",
        "_STLP_PRIV",
        "_STLP_TEMPLATE_NULL",
    ]

    @staticmethod
    def init():
        base_ext = SIXAnalyzer_rules.get_conf('extensions').replace('"', '').split(',')
        extensions = ""
        for ext in range(len(base_ext)):
            extensions += "-name \"" + base_ext[ext] + "\" "
            if (ext + 1 < len(base_ext)):
                extensions += "-or "
        SIXAnalyzer_rules.config.set(SIXAnalyzer_rules.namespace, 'extensions', extensions)

    @staticmethod
    def get_conf(key):
        try:
            value = SIXAnalyzer_rules.config.get(SIXAnalyzer_rules.namespace, key)
        except configparser.Error:
            print ("[DEBUG] No option '%s' found in namespace '%s'." %
                    (key, SIXAnalyzer_rules.namespace))
            return None

        try:
            return int(value)
        except ValueError:
            if value == 'True':
                return True
            elif value == 'False':
                return False
            else:
                if key == 'select-by-word':
                    value = b64decode(value)
                return value
