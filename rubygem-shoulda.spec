%global gem_name shoulda
Name:                rubygem-%{gem_name}
Version:             3.6.0
Release:             1
Summary:             Making tests easy on the fingers and eyes
License:             MIT
URL:                 https://github.com/thoughtbot/shoulda
Source0:             https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:       ruby(release) rubygems-devel ruby rubygem(jbuilder) rubygem(minitest-reporters)
BuildRequires:       rubygem(rails) rubygem(shoulda-context) rubygem(shoulda-matchers)
BuildRequires:       rubygem(sqlite3)
BuildArch:           noarch
%description
Making tests easy on the fingers and eyes.

%package doc
Summary:             Documentation for %{name}
Requires:            %{name} = %{version}-%{release}
BuildArch:           noarch
%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ln -sf %{_builddir}/%{gem_name}-%{version}.gemspec %{gem_name}.gemspec
cat << GF > Gemfile
source 'https://rubygems.org'
gem 'rails'
GF
sed -i "/require 'pry/ s/^/#/" test/test_helper.rb
sed -i "/current_bundle/ s/^/#/" test/acceptance_test_helper.rb
sed -i "/assert_appraisal/ s/^/#/" test/acceptance_test_helper.rb
sed -i '/rails new/ s/"$/ --skip-bootsnap --skip-listen --skip-puma --skip-spring --skip-sprockets"/' \
  test/support/acceptance/helpers/step_helpers.rb
sed -i "/updating_bundle do |bundle|/a \\
        bundle.remove_gem 'capybara'" test/support/acceptance/helpers/step_helpers.rb
sed -i "/updating_bundle do |bundle|/a \\
        bundle.remove_gem 'selenium-webdriver'" test/support/acceptance/helpers/step_helpers.rb
sed -i "/updating_bundle do |bundle|/a \\
        bundle.remove_gem 'chromedriver-helper'" test/support/acceptance/helpers/step_helpers.rb
sed -i '/ActiveRecord::Migration/ s/$/["5.2"]/' \
  test/acceptance/rails_integration_test.rb
sed -i 's/render nothing: true/head :ok/' \
  test/acceptance/rails_integration_test.rb
sed -i "/create_rails_application/a \\
    add_minitest_to_project" test/acceptance/rails_integration_test.rb
ruby -rpathname -Itest -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Appraisals
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/gemfiles
%{gem_instdir}/shoulda.gemspec
%{gem_instdir}/test

%changelog
* Wed Aug 19 2020 xiezheng <xiezheng4@huawei.com> - 3.6.0-1
- package init
