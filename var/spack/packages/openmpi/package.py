from spack import *

class Openmpi(Package):
    """Open MPI is a project combining technologies and resources from
       several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI)
       in order to build the best MPI library available. A completely
       new MPI-2 compliant implementation, Open MPI offers advantages
       for system and software vendors, application developers and
       computer science researchers.
    """

    homepage = 'http://www.open-mpi.org'

    url = 'http://www.open-mpi.org/software/ompi/v1.10/downloads/openmpi-1.10.0.tar.gz'
    #list_url = 'http://www.open-mpi.org/software/ompi'
    #list_depth = 2

    version('1.10.0', '10e097bfaca8ed625781af0314797b90')
    version('1.8.2', 'ab538ed8e328079d566fc797792e016e')
    version('1.6.5', '03aed2a4aa4d0b27196962a2a65fc475')

    patch('ad_lustre_rwcontig_open_source.patch', when="@1.6.5")
    patch('llnl-platforms.patch', when="@1.6.5")

    provides('mpi@:2')

    def url_for_version(self, version):
        """Handle OpenMPI URLs, which write the version two different ways."""
        parts = [str(p) for p in Version(version)]
        major_minor = ".".join(parts[:2])
        full = ".".join(parts)
        return "http://www.open-mpi.org/software/ompi/v%s/downloads/openmpi-%s.tar.gz" % (major_minor, full)

    def install(self, spec, prefix):
        config_args = ["--prefix=%s" % prefix]

        # TODO: use variants for this, e.g. +lanl, +llnl, etc.
        # use this for LANL builds, but for LLNL builds, we need:
        #     "--with-platform=contrib/platform/llnl/optimized"
        if self.version == ver("1.6.5") and '+lanl' in spec:
            config_args.append("--with-platform=contrib/platform/lanl/tlcc2/optimized-nopanasas")

        # TODO: Spack should make it so that you can't actually find
        # these compilers if they're "disabled" for the current
        # compiler configuration.
        if not self.compiler.f77 and not self.compiler.fc:
            config_args.append("--enable-mpi-fortran=no")

        configure(*config_args)
        make()
        make("install")
