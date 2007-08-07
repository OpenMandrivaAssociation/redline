%define section         free
%define gcj_support     1
%bcond_without          bootstrap

Name:           redline
Version:        1.0.10
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        Pure Java library for manipulating RPM Package Manager packages
License:        MIT
Group:          Development/Java
URL:            http://www.freecompany.org/
Source0:        http://repository.freecompany.org/org/freecompany/redline/zips/redline-src-1.0.10.zip
Source1:        redline-1.0.10-build.xml
Requires:       util-text
Requires:       util-xml-editor
BuildRequires:  ant
BuildRequires:  ant-junit
%if %without bootstrap
BuildRequires:  imp-core
%endif
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  junit
BuildRequires:  util-text
BuildRequires:  util-xml-editor
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Redline is a pure Java library for manipulating RPM Package Manager
packages. Currently the project supports reading and creating
packages and has an included Ant task useful for integration with
build systems. Support for package signatures will be added in a
future release.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%if %with bootstrap
%{__cp} -a %{SOURCE1} build.xml
%endif
%{__perl} -pi -e 's|<javac|<javac nowarn="true"|g' build.xml

%build
#export CLASSPATH=$(build-classpath junit brimstone-cache brimstone-core brimstone-main brimstone-module infoset util-multicaster xmlwriter)
export CLASSPATH=$(build-classpath junit util-xml-editor util-text)
%if %without bootstrap
export CLASSPATH=${CLASSPATH}:$(build-classpath imp-core)
%endif
export OPT_JAR_LIST="ant/ant-junit ant/ant-nodeps"
%{ant} jar javadoc test

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
