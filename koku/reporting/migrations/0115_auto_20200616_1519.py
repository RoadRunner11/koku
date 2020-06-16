# Generated by Django 2.2.12 on 2020-06-16 15:19
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("reporting", "0114_adding_source_uuid")]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE reporting_ocpusagelineitem_daily_summary_partitioned (
                id bigint NOT NULL,
                cluster_id character varying(50),
                namespace character varying(253),
                node character varying(253),
                usage_start date NOT NULL,
                usage_end date NOT NULL,
                pod_usage_cpu_core_hours numeric(27,9),
                pod_request_cpu_core_hours numeric(27,9),
                pod_limit_cpu_core_hours numeric(27,9),
                pod_usage_memory_gigabyte_hours numeric(27,9),
                pod_request_memory_gigabyte_hours numeric(27,9),
                pod_limit_memory_gigabyte_hours numeric(27,9),
                node_capacity_cpu_core_hours numeric(27,9),
                node_capacity_cpu_cores numeric(27,9),
                node_capacity_memory_gigabyte_hours numeric(27,9),
                node_capacity_memory_gigabytes numeric(27,9),
                cluster_capacity_cpu_core_hours numeric(27,9),
                cluster_capacity_memory_gigabyte_hours numeric(27,9),
                pod_labels jsonb,
                cluster_alias character varying(256),
                resource_id character varying(253),
                total_capacity_cpu_core_hours numeric(27,9),
                total_capacity_memory_gigabyte_hours numeric(27,9),
                data_source character varying(64),
                persistentvolume character varying(253),
                persistentvolumeclaim character varying(253),
                persistentvolumeclaim_capacity_gigabyte numeric(27,9),
                persistentvolumeclaim_capacity_gigabyte_months numeric(27,9),
                persistentvolumeclaim_usage_gigabyte_months numeric(27,9),
                storageclass character varying(50),
                volume_labels jsonb,
                volume_request_storage_gigabyte_months numeric(27,9),
                report_period_id integer,
                infrastructure_markup_cost numeric(33,15),
                infrastructure_monthly_cost numeric(33,15),
                infrastructure_project_markup_cost numeric(33,15),
                infrastructure_project_raw_cost numeric(33,15),
                infrastructure_raw_cost numeric(33,15),
                infrastructure_usage_cost jsonb,
                monthly_cost_type text,
                supplementary_monthly_cost numeric(33,15),
                supplementary_usage_cost jsonb,
                source_uuid uuid
            ) PARTITION BY RANGE (usage_start);


            ALTER TABLE reporting_ocpusagelineitem_daily_summary_partitioned OWNER TO kokuadmin;

            --
            -- Name: reporting_ocpusagelineitem_daily_summary_partitioned_id_seq; Type: SEQUENCE; Schema: acct10001; Owner: kokuadmin
            --

            CREATE SEQUENCE reporting_ocpusagelineitem_daily_summary_partitioned_id_seq
                START WITH 1
                INCREMENT BY 1
                NO MINVALUE
                NO MAXVALUE
                CACHE 1;


            ALTER TABLE reporting_ocpusagelineitem_daily_summary_partitioned_id_seq OWNER TO kokuadmin;

            --
            -- Name: reporting_ocpusagelineitem_daily_summary_partitioned_id_seq; Type: SEQUENCE OWNED BY; Schema: acct10001; Owner: kokuadmin
            --

            ALTER SEQUENCE reporting_ocpusagelineitem_daily_summary_partitioned_id_seq OWNED BY reporting_ocpusagelineitem_daily_summary_partitioned.id;


            --
            -- Name: reporting_ocpusagelineitem_daily_summary_partitioned id; Type: DEFAULT; Schema: acct10001; Owner: kokuadmin
            --

            ALTER TABLE ONLY reporting_ocpusagelineitem_daily_summary_partitioned ALTER COLUMN id SET DEFAULT nextval('reporting_ocpusagelineitem_daily_summary_partitioned_id_seq'::regclass);

            --
            -- Name: ocp_summaryp_namespace_like_idx; Type: INDEX; Schema: acct10001; Owner: kokuadmin
            --

            CREATE INDEX ocp_summaryp_namespace_like_idx ON reporting_ocpusagelineitem_daily_summary_partitioned USING gin (upper((namespace)::text) public.gin_trgm_ops);


            --
            -- Name: ocp_summaryp_node_like_idx; Type: INDEX; Schema: acct10001; Owner: kokuadmin
            --

            CREATE INDEX ocp_summaryp_node_like_idx ON reporting_ocpusagelineitem_daily_summary_partitioned USING gin (upper((node)::text) public.gin_trgm_ops);


            --
            -- Name: pod_labelsp_idx; Type: INDEX; Schema: acct10001; Owner: kokuadmin
            --

            CREATE INDEX pod_labelsp_idx ON reporting_ocpusagelineitem_daily_summary_partitioned USING gin (pod_labels);


            --
            -- Name: reporting_ocpusagelineitemp_report_period_idx; Type: INDEX; Schema: acct10001; Owner: kokuadmin
            --

            CREATE INDEX reporting_ocpusagelineitemp_report_period_idx ON reporting_ocpusagelineitem_daily_summary_partitioned USING btree (report_period_id);


            --
            -- Name: summaryp_data_source_idx; Type: INDEX; Schema: acct10001; Owner: kokuadmin
            --

            CREATE INDEX summaryp_data_source_idx ON reporting_ocpusagelineitem_daily_summary_partitioned USING btree (data_source);


            --
            -- Name: summaryp_namespace_idx; Type: INDEX; Schema: acct10001; Owner: kokuadmin
            --

            CREATE INDEX summaryp_namespace_idx ON reporting_ocpusagelineitem_daily_summary_partitioned USING btree (namespace varchar_pattern_ops);


            --
            -- Name: summaryp_node_idx; Type: INDEX; Schema: acct10001; Owner: kokuadmin
            --

            CREATE INDEX summaryp_node_idx ON reporting_ocpusagelineitem_daily_summary_partitioned USING btree (node varchar_pattern_ops);


            --
            -- Name: summaryp_ocp_usage_idx; Type: INDEX; Schema: acct10001; Owner: kokuadmin
            --

            CREATE INDEX summaryp_ocp_usage_idx ON reporting_ocpusagelineitem_daily_summary_partitioned USING btree (usage_start);


            --
            -- Name: reporting_ocpusagelineitem_daily_summary_partitioned reporting_ocpusageli_report_period_id_fc68baea_fk_reporting; Type: FK CONSTRAINT; Schema: acct10001; Owner: kokuadmin
            --

            ALTER TABLE reporting_ocpusagelineitem_daily_summary_partitioned
                ADD CONSTRAINT reporting_ocpusageli_report_period_id_fc68baea_fk_reporting FOREIGN KEY (report_period_id) REFERENCES reporting_ocpusagereportperiod(id) DEFERRABLE INITIALLY DEFERRED;

            CREATE TABLE reporting_ocpusagelineitem_daily_summary_partitioned_2020_05 PARTITION OF reporting_ocpusagelineitem_daily_summary_partitioned
            FOR VALUES FROM ('2020-05-01') TO ('2020-05-31');

            CREATE TABLE reporting_ocpusagelineitem_daily_summary_partitioned_2020_06 PARTITION OF reporting_ocpusagelineitem_daily_summary_partitioned
            FOR VALUES FROM ('2020-06-01') TO ('2020-06-30');

            """
        )
    ]